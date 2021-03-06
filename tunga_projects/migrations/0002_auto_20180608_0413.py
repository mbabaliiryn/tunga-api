# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 04:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tunga_projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'initial', b'Initial'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected')], default=b'initial', help_text='initial - Initial,accepted - Accepted,rejected - Rejected', max_length=20)),
                ('updates_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_participants_added', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'participation',
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects_owned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='pm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects_managed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tunga_projects.Project'),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='project_participants', through='tunga_projects.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('user', 'project')]),
        ),
    ]
