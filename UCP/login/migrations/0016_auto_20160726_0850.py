# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_userprofile_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='theme',
            field=models.CharField(default=b'cerulean', max_length=10, choices=[(b'cerulean', b'cerulean'), (b'journal', b'journal'), (b'flat', b'flat'), (b'readable', b'readable'), (b'paper', b'paper')]),
        ),
    ]
