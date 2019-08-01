# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-27 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_utils', '0025_auto_20181116_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='item',
            field=models.CharField(blank=True, choices=[('self_guided', 'Do-it-yourself'), ('onboarding', 'Tunga onboarding'), ('onboarding_special', 'Onboarding special offer'), ('project', 'Tunga project')], help_text='self_guided - Do-it-yourself,onboarding - Tunga onboarding,onboarding_special - Onboarding special offer,project - Tunga project', max_length=50, null=True),
        ),
    ]