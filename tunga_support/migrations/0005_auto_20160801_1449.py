# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 14:49
from __future__ import unicode_literals

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_support', '0004_auto_20160730_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportpage',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, help_text='Enter a comma-separated tag string', initial='', space_delimiter=False, to='tunga_support.SupportTag'),
        ),
    ]
