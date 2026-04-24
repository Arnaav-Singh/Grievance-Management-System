from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('hod', 'HOD'),
        ('dean', 'Dean'),
        ('admin', 'Admin'),
    )
    DEPARTMENT_CHOICES = (
        ('Academic', 'Academic'),
        ('Hostel', 'Hostel'),
        ('Infrastructure', 'Infrastructure'),
        ('Admin', 'Admin'),
        ('Other', 'Other'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True)

class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ('Academic', 'Academic'),
        ('Hostel', 'Hostel'),
        ('Infrastructure', 'Infrastructure'),
        ('Admin', 'Admin'),
        ('Other', 'Other'),
    )
    LOCATION_CHOICES = (
        ('Boys Hostels', (
            ('Block 1 (Boys)', 'Block 1'),
            ('Block 2 (Boys)', 'Block 2'),
            ('Block 3 (Boys)', 'Block 3'),
            ('Block 4 (Boys)', 'Block 4'),
            ('Block 5 (Boys)', 'Block 5'),
            ('Block 6 (Boys)', 'Block 6'),
            ('Block 7 (Boys)', 'Block 7'),
            ('Block 8 (Boys)', 'Block 8'),
            ('Block 9 (Boys)', 'Block 9'),
            ('Block 10 (Boys)', 'Block 10'),
            ('Block 14 (Boys)', 'Block 14'),
            ('Block 15 (Boys)', 'Block 15'),
            ('Block 16 (Boys)', 'Block 16'),
            ('Block 17 (Boys)', 'Block 17'),
            ('Block 18 (Boys)', 'Block 18'),
            ('Block 19 (Boys)', 'Block 19'),
            ('Block 20 (Boys)', 'Block 20'),
        )),
        ('Girls Hostels', (
            ('Block 11 (Girls)', 'Block 11'),
            ('Block 12 (Girls)', 'Block 12'),
            ('Block 13 (Girls)', 'Block 13'),
            ('Block 21 (Girls)', 'Block 21'),
            ('Block 22 (Girls)', 'Block 22'),
        )),
        ('Other Locations', (
            ('Library', 'Library'),
            ('Lab 1', 'Lab 1'),
            ('Main Gate', 'Main Gate'),
            ('Cafeteria', 'Cafeteria'),
            ('Other', 'Other'),
        )),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Escalated', 'Escalated'),
    )
    
    GENDER_CHOICES = (
        ('Boys', 'Boys'),
        ('Girls', 'Girls'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_complaints')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Other')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    deadline = models.DateTimeField(blank=True, null=True)
    escalation_level = models.IntegerField(default=0) # 0: Staff, 1: HOD, 2: Dean
    
    admin_remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            # Auto-routing logic
            if not self.assigned_to:
                eligible_admins = User.objects.filter(department=self.category, role__in=['staff', 'hod', 'dean', 'admin'])
                if not eligible_admins.exists():
                    # Fallback to any admin-level user
                    eligible_admins = User.objects.filter(role__in=['staff', 'hod', 'dean', 'admin'])
                
                if eligible_admins.exists():
                    best_admin = eligible_admins.annotate(
                        active_count=Count('assigned_complaints', filter=Q(assigned_complaints__status__in=['Pending', 'In Progress', 'Escalated']))
                    ).order_by('active_count').first()
                    self.assigned_to = best_admin
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
