# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-15 10:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_projects', '0014_auto_20180715_0951'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectmeta',
            unique_together=set([('project', 'meta_key')]),
        ),
    ]
