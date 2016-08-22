# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_remove_userprofile_theme'),
        ('news_event', '0007_auto_20160730_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='posted_by',
            field=models.ForeignKey(to='login.UserProfile', null=True),
        ),
    ]
