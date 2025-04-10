from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import  uuid
from rate_management.models import CurrencyPair

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class ClientConfig(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name=('config'))
    rate_limit = models.PositiveIntegerField(default=60) # 60 requests per minute
    quota_limit = models.PositiveIntegerField(default=1000) # 1000 requests per day
    allowed_pairs = models.ManyToManyField(CurrencyPair, blank=True)

    def __str__(self):
        return f"Config for {self.client.company_name}"

class ApiKey(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_valid(self):  # Check if the API key is valid
        if not self.is_active:
            return False
        if self.expiry_date and timezone.now() > self.expiry_date:
            return False
        return True

    def __str__(self):
        return f"API Key for {self.client.company_name}"

class Usage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='usage')
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    request_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['client', 'timestamp']),
            models.Index(fields=['client', 'currency_pair', 'timestamp']),
        ]

    def __str__(self):
        return f"Usage for {self.client.company_name} on {self.currency_pair.pair_symbol} at {self.timestamp}"
