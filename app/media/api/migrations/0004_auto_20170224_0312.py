# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-24 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170223_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='access_level',
            field=models.CharField(choices=[('0', 'GUEST'), ('1', 'USER'), ('2', 'FRIEND'), ('4', 'MODERATOR'), ('9', 'ADMIN')], default=0, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
    ]