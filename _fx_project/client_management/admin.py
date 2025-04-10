from django.contrib import admin
from .models import Client, ClientConfig, ApiKey, Usage

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_active')
    list_filter = ['is_active']
    search_fields = ['company_name', 'user__username', 'user__email']


@admin.register(ClientConfig)
class ClientConfigAdmin(admin.ModelAdmin):
    list_display = ('client', 'rate_limit', 'quota_limit')
    filter_horizontal = ['allowed_pairs']


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at', 'expiry_date', 'is_active')
    list_filter = ['is_active']
    search_fields = ['client__company_name']
    readonly_fields = ['key']


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('client', 'currency_pair', 'timestamp', 'request_count')
    list_filter = ['client']
    search_fields = ['client__company_name', 'currency_pair__pair_symbol']
    date_hierarchy = 'timestamp'
