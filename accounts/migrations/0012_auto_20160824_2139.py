# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-24 21:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_carddata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialaccount',
            name='social_network',
        ),
        migrations.RemoveField(
            model_name='socialaccount',
            name='user',
        ),
        migrations.DeleteModel(
            name='SocialAccount',
        ),
        migrations.DeleteModel(
            name='SocialNetwork',
        ),
    ]