# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 11:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_auto_20160616_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsphotos',
            name='good',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods_photos', to='goods.Good'),
        ),
    ]
