# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-12 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('description', models.CharField(max_length=255)),
                ('is_completed', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
