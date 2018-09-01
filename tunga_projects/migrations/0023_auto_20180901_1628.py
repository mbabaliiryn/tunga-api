# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-01 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_projects', '0022_auto_20180825_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interestpoll',
            name='status',
            field=models.CharField(choices=[(b'initial', 'Initial'), (b'interested', 'Interested'), (b'uninterested', 'Uninterested')], default=b'initial', help_text='initial - Initial,interested - Interested,uninterested - Uninterested', max_length=20),
        ),
    ]
