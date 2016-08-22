# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('news_event', '0002_auto_20160729_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=tinymce.models.HTMLField(null=True, blank=True),
        ),
    ]
