# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_auto_20160604_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='size',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='uploaded_file',
            field=models.FileField(upload_to=b'user-attachments'),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='no_of_replies',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='no_of_views',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='posted_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 18, 14, 9, 10, 804912, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='posted_by',
            field=models.ForeignKey(to='login.UserProfile', null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='posted_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 18, 14, 9, 10, 806023, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='posted_by',
            field=models.ForeignKey(to='login.UserProfile', null=True),
        ),
    ]
