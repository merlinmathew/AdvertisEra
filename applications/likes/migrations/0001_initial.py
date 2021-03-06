# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 05:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='advertisements.Advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Likes',
                'verbose_name': 'Like',
            },
        ),
    ]
