# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-06-18 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20180609_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedcontentitem',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
