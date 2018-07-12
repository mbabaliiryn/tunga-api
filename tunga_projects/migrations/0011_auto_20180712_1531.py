# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_projects', '0010_auto_20180712_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressevent',
            name='type',
            field=models.CharField(choices=[(b'developer', b'Developer Update'), (b'pm', b'PM Report'), (b'client', b'Client Survey'), (b'milestone', b'Milestone'), (b'internal', b'Internal Milestone')], default=b'developer', help_text='developer - Developer Update,pm - PM Report,client - Client Survey,milestone - Milestone,internal - Internal Milestone', max_length=50),
        ),
    ]
