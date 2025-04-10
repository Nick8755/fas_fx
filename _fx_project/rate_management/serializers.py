from rest_framework import serializers
from .models import Provider, Currency, CurrencyPair, Rate

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ['id', 'name', 'api_endpoint', 'is_active', 'timeout']

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol', 'is_active']

class CurrencyPairSerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer()
    quote_currency = CurrencySerializer()
    supported_providers = ProviderSerializer(many=True)

    class Meta:
        model = CurrencyPair
        fields = ['id', 'base_currency', 'quote_currency', 'supported_providers', 'pair_symbol', 'is_active']

class RateReadSerializer(serializers.ModelSerializer):
    currency_pair = CurrencyPairSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = Rate
        fields = '__all__'

class RateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'currency_pair', 'provider', 'value', 'operation_type', 'last_updated', 'is_live']

