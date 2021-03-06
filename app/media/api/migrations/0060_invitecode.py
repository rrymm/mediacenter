# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-21 02:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_merge_20180821_0211'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('uses', models.IntegerField(default=1)),
                ('invitees', models.ManyToManyField(related_name='_invitecode_invitees_+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
