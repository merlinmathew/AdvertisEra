# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 05:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_advertisement', to=settings.AUTH_USER_MODEL),
        ),
    ]