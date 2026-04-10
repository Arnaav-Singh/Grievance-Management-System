from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_django/', admin.site.urls), # Renamed to avoid collision with our admin dashboard
    path('', include('core.urls')),
]
