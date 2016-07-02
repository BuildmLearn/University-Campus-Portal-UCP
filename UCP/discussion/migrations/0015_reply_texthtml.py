# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0014_auto_20160701_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='textHTML',
            field=tinymce.models.HTMLField(default=''),
            preserve_default=False,
        ),
    ]
