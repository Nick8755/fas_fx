# Generated by Django 5.1.5 on 2025-03-23 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_management', '0001_initial'),
        ('rate_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientBilling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('total_requests', models.PositiveIntegerField(default=0)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='billing', to='client_management.client')),
            ],
        ),
        migrations.CreateModel(
            name='RateUsageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_usage_logs', to='client_management.client')),
                ('currency_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_management.currencypair')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_management.provider')),
            ],
            options={
                'indexes': [models.Index(fields=['client', 'timestamp'], name='billing_ana_client__17c1f8_idx'), models.Index(fields=['client', 'currency_pair', 'timestamp'], name='billing_ana_client__c1e2f9_idx')],
            },
        ),
    ]
