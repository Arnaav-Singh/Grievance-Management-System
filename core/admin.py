from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Complaint

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'department', 'is_staff')
    list_filter = ('role', 'department', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role', 'department')}),
    )

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'category', 'location', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
