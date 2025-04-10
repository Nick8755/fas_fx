from django.contrib import admin
from .models import RateUsageLog, ClientBilling

@admin.register(RateUsageLog)
class RateUsageLogAdmin(admin.ModelAdmin):
    list_display = ('client', 'currency_pair', 'provider', 'operation_type', 'timestamp', 'request_count')
    list_filter = ['client', 'provider', 'operation_type']
    search_fields = ['client__company_name']
    date_hierarchy = 'timestamp'



@admin.register(ClientBilling)
class ClientBillingAdmin(admin.ModelAdmin):
    list_display = ('client', 'period_start', 'period_end', 'total_requests', 'total_cost', 'is_paid', 'created_at')
    list_filter = ['client', 'is_paid']
    search_fields = ['client__company_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['total_requests', 'total_cost']