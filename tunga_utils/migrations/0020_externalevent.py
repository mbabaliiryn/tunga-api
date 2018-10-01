# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-15 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_utils', '0019_auto_20180814_0103'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('hubspot', 'HubSpot')], help_text='hubspot - HubSpot', max_length=50)),
                ('payload', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notification_sent_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]