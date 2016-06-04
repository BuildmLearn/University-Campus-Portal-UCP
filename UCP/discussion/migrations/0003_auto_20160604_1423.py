# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0002_discussionthread_last_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionthread',
            name='last_reply',
            field=models.ForeignKey(related_name='last_reply', blank=True, to='discussion.Reply', null=True),
        ),
    ]
