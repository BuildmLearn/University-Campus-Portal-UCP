# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0012_auto_20160623_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='text',
            field=models.CharField(default=b'', max_length=b'1000'),
        ),
    ]
