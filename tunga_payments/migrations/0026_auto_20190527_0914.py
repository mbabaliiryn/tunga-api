# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-27 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_payments', '0025_auto_20190219_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.CharField(choices=[('EUR', 'EUR')], default='EUR', max_length=15),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(blank=True, choices=[(None, 'Any'), ('stripe', 'Pay with Stripe'), ('bitonic', 'Pay with iDeal / mister cash'), ('bitcoin', 'Pay with BitCoin'), ('bank', 'Pay by bank transfer')], help_text='None - Any,stripe - Pay with Stripe,bitonic - Pay with iDeal / mister cash,bitcoin - Pay with BitCoin,bank - Pay by bank transfer', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('canceled', 'Canceled')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='type',
            field=models.CharField(choices=[('sale', 'Sales Invoice'), ('purchase', 'Purchase Invoice'), ('client', 'Client'), ('tunga', 'Tunga'), ('developer', 'Developer'), ('credit_nota', 'Credit Nota')], max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('EUR', 'EUR')], default='EUR', max_length=15),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('stripe', 'Stripe'), ('bank', 'Bank Transfer'), ('bitcoin', 'Bitcoin'), ('bitonic', 'Bitonic')], max_length=150),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('completed', 'Completed'), ('failed', 'Failed'), ('retry', 'Retry')], default='initiated', max_length=50),
        ),
    ]