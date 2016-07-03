# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0017_discussionthread_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussionthread',
            name='tag',
        ),
        migrations.AddField(
            model_name='discussionthread',
            name='tag',
            field=models.ManyToManyField(to='discussion.Tag'),
        ),
    ]
