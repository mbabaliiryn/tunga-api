# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-27 09:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tunga_settings', '0002_auto_20160511_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userswitchsetting',
            name='setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tunga_settings.SwitchSetting'),
        ),
        migrations.AlterField(
            model_name='uservisibilitysetting',
            name='setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tunga_settings.VisibilitySetting'),
        ),
    ]