from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Complaint

class StudentSignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial='student')
    department = forms.ChoiceField(choices=User.DEPARTMENT_CHOICES, required=False, initial='Other')
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'department', 'email', 'first_name', 'last_name')

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'location', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter complaint title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your complaint...'}),
        }

class AdminComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'admin_remark']
