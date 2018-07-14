# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-07-02 23:12
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_feedcontentitem_visibility'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=140)),
                ('description', models.TextField(blank=True)),
                ('position', django.contrib.gis.db.models.fields.GeometryField(geography=True, srid=4326)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceRestriction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_distance', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('place', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Place')),
            ],
        ),
        migrations.AddField(
            model_name='feed',
            name='places',
            field=models.ManyToManyField(blank=True, to='api.PlaceRestriction'),
        ),
        migrations.AddField(
            model_name='feedcontentitem',
            name='places',
            field=models.ManyToManyField(blank=True, to='api.PlaceRestriction'),
        ),
        migrations.AddField(
            model_name='profile',
            name='places',
            field=models.ManyToManyField(blank=True, to='api.PlaceRestriction'),
        ),
    ]
