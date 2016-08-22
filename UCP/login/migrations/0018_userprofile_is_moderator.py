# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_remove_userprofile_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_moderator',
            field=models.BooleanField(default=True),
        ),
    ]
