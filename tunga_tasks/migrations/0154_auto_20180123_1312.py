# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-23 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_tasks', '0153_task_exclude_payment_costs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dev_rate',
            field=models.DecimalField(decimal_places=4, default=20, max_digits=19),
        ),
        migrations.AlterField(
            model_name='task',
            name='exclude_payment_costs',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='pm_rate',
            field=models.DecimalField(decimal_places=4, default=40, max_digits=19),
        ),
    ]
