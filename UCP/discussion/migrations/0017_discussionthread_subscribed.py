# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_auto_20160623_1559'),
        ('discussion', '0016_remove_reply_texthtml'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionthread',
            name='subscribed',
            field=models.ManyToManyField(related_name='subscribed', to='login.UserProfile'),
        ),
    ]
