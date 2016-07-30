# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news_event', '0005_event_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=b'event_images'),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
