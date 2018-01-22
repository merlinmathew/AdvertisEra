# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-19 12:39
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_auto_20180117_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
    ]
