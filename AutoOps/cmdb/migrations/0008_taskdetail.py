# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_remove_taskmanage_cmds'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('task_cmds', models.CharField(max_length=50)),
                ('task_result', models.CharField(max_length=300)),
                ('task_status', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=100)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.TaskManage')),
            ],
        ),
    ]
