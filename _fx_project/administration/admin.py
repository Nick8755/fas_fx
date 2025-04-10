from django.contrib import admin
from .models import AdminUser

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'is_active', 'created_at')
    list_filter = ['role', 'department', 'is_active']
    search_fields = ['user__username', 'department']