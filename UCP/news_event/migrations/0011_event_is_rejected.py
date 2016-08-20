# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_event', '0010_event_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
