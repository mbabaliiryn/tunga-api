# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-15 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_pages', '0014_auto_20180215_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]