# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_event', '0008_news_posted_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-posted_at']},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-posted_at']},
        ),
    ]
