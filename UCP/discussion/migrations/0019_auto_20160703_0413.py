# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0018_auto_20160703_0411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussionthread',
            old_name='tag',
            new_name='tags',
        ),
    ]
