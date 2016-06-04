# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_auto_20160604_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionthread',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
