# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-31 21:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20180531_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='group',
        ),
    ]