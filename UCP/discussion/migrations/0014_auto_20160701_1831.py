# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0013_auto_20160623_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['-posted_at']},
        ),
    ]
