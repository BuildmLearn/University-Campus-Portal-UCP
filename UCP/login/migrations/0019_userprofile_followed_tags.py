# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_auto_20160703_0413'),
        ('login', '0018_userprofile_is_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followed_tags',
            field=models.ManyToManyField(to='discussion.Tag', null=True),
        ),
    ]
