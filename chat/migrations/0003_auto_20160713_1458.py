# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_thread_has_unread'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ('-last_message',)},
        ),
    ]
