# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dev_id', models.CharField(verbose_name='Device ID', max_length=50, unique=True)),
                ('dev_type', models.CharField(blank=True, null=True, verbose_name='Device Type', max_length=255,
                                              choices=[('IOS', 'iOS'), ('ANDROID', 'Android')])),
                ('reg_id', models.CharField(verbose_name='Registration ID', max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('modified_date', models.DateTimeField(verbose_name='Modified date', auto_now=True)),
                ('is_active', models.BooleanField(verbose_name='Is active?', default=False)),
            ],
            options={
                'verbose_name_plural': 'Devices',
                'ordering': ['-modified_date'],
                'abstract': False,
                'verbose_name': 'Device',
            },
        ),
    ]
