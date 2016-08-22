# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_auto_20160703_0413'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.CharField(max_length=10000, blank=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tags', models.ManyToManyField(to='discussion.Tag')),
            ],
        ),
    ]
