# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=1),
        ),
    ]