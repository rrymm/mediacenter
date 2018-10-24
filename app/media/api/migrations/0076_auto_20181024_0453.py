# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-24 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_notification_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=models.CharField(choices=[('Img00', 'create_image'), ('Img01', 'read_image'), ('Img02', 'update_image'), ('Img03', 'delete_image'), ('Img04', 'comment_image'), ('Img05', 'save_image'), ('Link00', 'create_link'), ('Link01', 'read_link'), ('Link02', 'update_link'), ('Link03', 'delete_link'), ('Link04', 'comment_link'), ('Link05', 'save_link'), ('Topic00', 'create_topic'), ('Topic01', 'read_topic'), ('Topic02', 'update_topic'), ('Topic03', 'delete_topic'), ('Topic05', 'save_topic'), ('Post00', 'create_post'), ('Post02', 'update_post'), ('Post03', 'delete_post'), ('Post05', 'save_post'), ('Poll00', 'create_poll'), ('Poll01', 'read_poll'), ('Poll02', 'update_poll'), ('Poll03', 'delete_poll'), ('Poll05', 'save_poll'), ('Poll06', 'vote_poll'), ('BlogP00', 'create_blogpost'), ('BlogP01', 'read_blogpost'), ('BlogP02', 'update_blogpost'), ('BlogP03', 'delete_blogpost'), ('BlogP04', 'comment_blogpost'), ('BlogP05', 'save_blogpost'), ('Profile04', 'comment_profile'), ('Int00', 'create_interest'), ('Int02', 'update_interest'), ('Int05', 'save_interest')], max_length=8),
        ),
    ]
