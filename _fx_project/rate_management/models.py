from django.db import models
from django.utils import timezone


class Provider(models.Model):
    name = models.CharField(max_length=100) # e.g. "Open Exchange Rates"
    api_endpoint = models.URLField(blank=True, null=True) # e.g. "https://openexchangerates.org/api/latest.json"
    api_key = models.CharField(max_length=255, blank=True, null=True) # e.g. "1234567890"
    is_active = models.BooleanField(default=True) # we can switch off the provider if we want to stop using it
    refresh_interval = models.IntegerField(default=60) #60 seconds
    timeout = models.IntegerField(default=5) #5 seconds for the request to timeout from the provider
    retry_count = models.IntegerField(default=3) #3 retries before giving up
    created_at = models.DateTimeField(auto_now_add=True) # e.g. "2021-09-01T00:00:00Z"
    updated_at = models.DateTimeField(auto_now=True) # e.g. "2021-09-01T00:00:00Z"

    def __str__(self):
        return self.name

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True) # e.g. "USD"
    name = models.CharField(max_length=100) # e.g. "United States Dollar"
    symbol = models.CharField(max_length=10, blank=True) # e.g. "$"
    decimal_places = models.PositiveSmallIntegerField(default=2) # e.g. 2
    is_active = models.BooleanField(default=True) # we can switch off the currency if we want to stop using it

    def __str__(self):
        return self.code

class CurrencyPair(models.Model):
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_pairs')
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='quote_pairs')
    supported_providers = models.ManyToManyField(Provider)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('base_currency', 'quote_currency')

    @property
    def pair_symbol(self):
        return f"{self.base_currency.code}/{self.quote_currency.code}"

    def __str__(self):
        return self.pair_symbol

class Rate(models.Model):
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE, related_name='rates')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='rates')
    value = models.DecimalField(max_digits=20, decimal_places=8)

    operation_type = models.CharField(
        max_length=10,
        choices=[
            ('buy', 'Buy'),
            ('sell', 'Sell')],
        default='buy'
    )

    timestamp = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['currency_pair', 'provider', 'timestamp']),
            models.Index(fields=['currency_pair', 'operation_type', 'timestamp'])
        ]
        ordering = ['-timestamp']

    def is_stale(self, max_age_seconds=60): # check if the rate is older than 60 seconds
        age = (timezone.now() - self.timestamp).total_seconds()
        return age > max_age_seconds

    def __str__(self):
        return f"{self.currency_pair.pair_symbol} - {self.value} - {self.provider.name}"