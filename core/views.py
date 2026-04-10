from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Avg, F
from django.core.paginator import Paginator
from .models import Complaint, User
from .forms import StudentSignupForm, ComplaintForm, AdminComplaintUpdateForm
from .utils import check_and_escalate_complaints
import json

def is_admin(user):
    return user.role in ['admin', 'staff', 'hod', 'dean']

def is_student(user):
    return user.role == 'student'

def signup_view(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = StudentSignupForm()
    return render(request, 'auth/signup.html', {'form': form})

@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='Pending').count(),
        'in_progress': complaints.filter(status='In Progress').count(),
        'resolved': complaints.filter(status='Resolved').count(),
        'escalated': complaints.filter(status='Escalated').count(),
    }
    return render(request, 'dashboards/student.html', {'complaints': complaints, 'stats': stats})

@login_required
@user_passes_test(is_student)
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, f"Complaint submitted successfully and assigned to {complaint.assigned_to.username if complaint.assigned_to else 'Support Team'}.")
            return redirect('student_dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'dashboards/submit_complaint.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    check_and_escalate_complaints()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    overdue = request.GET.get('overdue', '')
    
    # Filtering complaints based on role and department
    if request.user.role == 'admin':
        complaints = Complaint.objects.all().order_by('-created_at')
    else:
        # Show assigned complaints OR complaints in their department
        complaints = Complaint.objects.filter(
            Q(assigned_to=request.user) | Q(category=request.user.department)
        ).distinct().order_by('-created_at')
    
    if query:
        complaints = complaints.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        complaints = complaints.filter(category=category)
    if status:
        complaints = complaints.filter(status=status)
    if overdue == '1':
        from django.utils import timezone
        complaints = complaints.filter(deadline__lt=timezone.now(), status__in=['Pending', 'In Progress', 'Escalated'])
        
    # Stats should also be filtered for non-super-admins
    if request.user.role == 'admin':
        base_stats_query = Complaint.objects.all()
    else:
        base_stats_query = Complaint.objects.filter(
            Q(assigned_to=request.user) | Q(category=request.user.department)
        ).distinct()

    stats = {
        'total': base_stats_query.count(),
        'pending': base_stats_query.filter(status='Pending').count(),
        'resolved': base_stats_query.filter(status='Resolved').count(),
        'escalated': base_stats_query.filter(status='Escalated').count(),
    }
    
    categories = Complaint.CATEGORY_CHOICES
    
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboards/admin.html', {
        'complaints': page_obj, 
        'stats': stats,
        'categories': categories,
        'selected_category': category,
        'selected_status': status,
        'query': query,
        'overdue': overdue,
        'page_obj': page_obj
    })

@login_required
@user_passes_test(is_admin)
def admin_leaderboard(request):
    # Calculate performance metrics
    # average_resolution_time calculation: simplified as (updated_at - created_at) for Resolved complaints
    # In SQLite, duration math is tricky, so we'll do it in Python if needed or use ExpressionWrapper
    
    admins = User.objects.filter(role__in=['staff', 'hod', 'dean', 'admin']).annotate(
        resolved_count=Count('assigned_complaints', filter=Q(assigned_complaints__status='Resolved')),
        total_assigned=Count('assigned_complaints')
    ).order_by('-resolved_count')
    
    return render(request, 'analytics/leaderboard.html', {'admins': admins})

@login_required
@user_passes_test(is_admin)
def complaint_analytics(request):
    # Data for Heatmap (Complaints per Location)
    location_data = Complaint.objects.values('location').annotate(count=Count('id')).order_by('-count')
    
    labels = [item['location'] for item in location_data]
    counts = [item['count'] for item in location_data]
    
    # Category Distribution
    category_data = Complaint.objects.values('category').annotate(count=Count('id'))
    cat_labels = [item['category'] for item in category_data]
    cat_counts = [item['count'] for item in category_data]
    
    context = {
        'labels': json.dumps(labels),
        'counts': json.dumps(counts),
        'cat_labels': json.dumps(cat_labels),
        'cat_counts': json.dumps(cat_counts),
    }
    return render(request, 'analytics/heatmap.html', context)

# Re-including other views...
@login_required
@user_passes_test(is_student)
def edit_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, user=request.user)
    if complaint.status != 'Pending':
        messages.error(request, "You can only edit pending complaints.")
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, "Complaint updated successfully!")
            return redirect('student_dashboard')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'dashboards/edit_complaint.html', {'form': form, 'complaint': complaint})

@login_required
@user_passes_test(is_student)
def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, user=request.user)
    if complaint.status != 'Pending':
        messages.error(request, "You can only delete pending complaints.")
    else:
        complaint.delete()
        messages.success(request, "Complaint deleted successfully!")
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_admin)
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = AdminComplaintUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, f"Complaint #{pk} updated successfully!")
            return redirect('admin_dashboard')
    return redirect('admin_dashboard')
