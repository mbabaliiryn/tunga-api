# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-13 23:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_tasks', '0114_auto_20170710_0857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeentry',
            options={'ordering': ['spent_at'], 'verbose_name_plural': 'time entries'},
        ),
        migrations.AlterModelOptions(
            name='workactivity',
            options={'verbose_name_plural': 'work activities'},
        ),
    ]