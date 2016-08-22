# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_auto_20160703_0413'),
        ('news_event', '0003_auto_20160729_0649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', tinymce.models.HTMLField(null=True, blank=True)),
                ('posted_at', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tags', models.ManyToManyField(to='discussion.Tag')),
            ],
        ),
    ]
