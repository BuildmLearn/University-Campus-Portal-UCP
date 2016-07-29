# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_remove_userprofile_theme'),
        ('news_event', '0004_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='posted_by',
            field=models.ForeignKey(to='login.UserProfile', null=True),
        ),
    ]
