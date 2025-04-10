from django.db import models
from client_management.models import Client
from rate_management.models import CurrencyPair, Provider

class RateUsageLog(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rate_usage_logs')
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    timestamp = models.DateTimeField(auto_now_add=True)
    request_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['client', 'timestamp']),
            models.Index(fields=['client', 'currency_pair', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.client.company_name} | {self.operation_type.upper()} | {self.currency_pair.pair_symbol} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class ClientBilling(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='billing')
    period_start = models.DateField()
    period_end = models.DateField()
    total_requests = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for {self.client.company_name} ({self.period_start} - {self.period_end})"