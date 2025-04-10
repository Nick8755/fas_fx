from django.contrib import admin
from .models import Provider, Currency, CurrencyPair, Rate

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'refresh_interval')
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'is_active')
    list_filter = ['is_active']
    search_fields = ['code', 'name']


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ('pair_symbol', 'is_active')
    list_filter = ['is_active']
    search_fields = ['base_currency__code', 'quote_currency__code'] # search by currency code via foreign key in CurrencyPair
    filter_horizontal = ['supported_providers']


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'provider', 'value', 'operation_type', 'timestamp', 'is_live')
    list_filter = ['is_live', 'provider', 'operation_type']
    search_fields = ['currency_pair__base_currency__code', 'currency_pair__quote_currency__code']
    date_hierarchy = 'timestamp'