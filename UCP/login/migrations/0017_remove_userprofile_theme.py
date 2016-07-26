# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20160726_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='theme',
        ),
    ]
