# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-06-21 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_feed_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedcontentitem',
            name='visibility',
            field=models.CharField(choices=[('0', 'Public'), ('1', 'Unlisted'), ('9', 'Private')], default='0', max_length=2),
        ),
    ]
