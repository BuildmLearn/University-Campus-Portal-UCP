# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_auto_20160623_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='reply',
            field=models.ForeignKey(related_name='attachment', to='discussion.Reply'),
        ),
    ]
