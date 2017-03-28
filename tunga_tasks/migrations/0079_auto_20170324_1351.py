# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_tasks', '0078_auto_20170324_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dev_rate',
            field=models.DecimalField(decimal_places=4, default=19, max_digits=19),
        ),
        migrations.AlterField(
            model_name='task',
            name='pm_rate',
            field=models.DecimalField(decimal_places=4, default=39, max_digits=19),
        ),
        migrations.AlterField(
            model_name='task',
            name='tunga_percentage_dev',
            field=models.DecimalField(decimal_places=4, default=34.21, max_digits=19),
        ),
        migrations.AlterField(
            model_name='task',
            name='tunga_percentage_pm',
            field=models.DecimalField(decimal_places=4, default=48.71, max_digits=19),
        ),
    ]