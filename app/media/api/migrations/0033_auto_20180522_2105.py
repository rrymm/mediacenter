# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-22 21:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20180516_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.GroupForum'),
        ),
    ]
