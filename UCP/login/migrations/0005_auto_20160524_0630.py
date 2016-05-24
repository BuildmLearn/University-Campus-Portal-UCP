# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20160524_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailvericationcode',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2016, 5, 25, 6, 30, 56, 580668)),
        ),
    ]
