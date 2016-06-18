# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0006_auto_20160618_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionthread',
            name='posted_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='posted_by',
            field=models.ForeignKey(blank=True, to='login.UserProfile', null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='posted_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reply',
            name='posted_by',
            field=models.ForeignKey(blank=True, to='login.UserProfile', null=True),
        ),
    ]
