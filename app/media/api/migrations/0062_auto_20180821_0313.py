# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-21 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20180821_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitecode',
            name='max_uses',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='invitecode',
            name='uses',
            field=models.IntegerField(default=0),
        ),
    ]
