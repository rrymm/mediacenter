# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-26 20:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170325_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
