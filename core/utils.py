from django.utils import timezone
from .models import Complaint, User
from django.db.models import Count, Q

def check_and_escalate_complaints():
    now = timezone.now()
    # Find active complaints past their deadline
    overdue_complaints = Complaint.objects.filter(
        status__in=['Pending', 'In Progress', 'Escalated'],
        deadline__lt=now
    )
    
    for complaint in overdue_complaints:
        # Hierarchy: 0 (Staff) -> 1 (HOD) -> 2 (Dean)
        if complaint.escalation_level < 2:
            complaint.escalation_level += 1
            complaint.status = 'Escalated'
            
            # New target role
            new_role = 'hod' if complaint.escalation_level == 1 else 'dean'
            
            # Find potential assignees
            eligible_admins = User.objects.filter(department=complaint.category, role=new_role)
            if not eligible_admins.exists():
                eligible_admins = User.objects.filter(role=new_role)
            
            if eligible_admins.exists():
                best_admin = eligible_admins.annotate(
                    active_count=Count('assigned_complaints', filter=Q(assigned_complaints__status__in=['Pending', 'In Progress', 'Escalated']))
                ).order_by('active_count').first()
                complaint.assigned_to = best_admin
                
                # Reset deadline for the next level (another 48 hours)
                from datetime import timedelta
                complaint.deadline = now + timedelta(hours=48)
                complaint.save()
