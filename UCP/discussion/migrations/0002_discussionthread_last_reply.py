# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionthread',
            name='last_reply',
            field=models.ForeignKey(related_name='last_reply', to='discussion.Reply', null=True),
        ),
    ]
