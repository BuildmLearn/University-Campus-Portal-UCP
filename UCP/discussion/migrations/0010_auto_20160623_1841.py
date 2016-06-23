# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0009_auto_20160623_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='size',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
