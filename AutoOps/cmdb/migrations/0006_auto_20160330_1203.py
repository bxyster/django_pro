# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_taskmanage_cron_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmanage',
            name='cron_type',
            field=models.CharField(choices=[(1, '\u547d\u4ee4\u6267\u884c'), (2, '\u811a\u672c\u6267\u884c')], max_length=10),
        ),
    ]
