# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-30 15:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_blocklist', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='blocked_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('complaint_type', models.SmallIntegerField(choices=[(0, 'Not defined'), (1, 'Owner profile is impersonating another'), (2, 'Fraud'), (3, 'Spam'), (4, 'Advertising page clog up search')], default=0)),
                ('complaint_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_complaints', to=settings.AUTH_USER_MODEL)),
                ('complaint_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_me_complaints', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
