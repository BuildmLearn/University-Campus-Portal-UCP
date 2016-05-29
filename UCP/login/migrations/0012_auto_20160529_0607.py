# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20160526_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='designation',
            field=models.CharField(default=b'Student', max_length=10, choices=[(b'Teacher', b'Teacher'), (b'Student', b'Student')]),
        ),
    ]
