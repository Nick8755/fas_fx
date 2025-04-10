from django.db import models
from django.contrib.auth.models import User


class AdminUser(models.Model):
    employee_types = [
        ('superadmin', 'Super Admin'),
        ('support', 'Support'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('audit', 'Audit'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=employee_types,
        default='support'
    )
    department = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
