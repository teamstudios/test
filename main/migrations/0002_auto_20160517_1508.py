# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 15:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SocialAccounts',
            new_name='SocialAccount',
        ),
    ]
