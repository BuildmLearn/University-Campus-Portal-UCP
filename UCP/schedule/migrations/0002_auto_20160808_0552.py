# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['-posted_at']},
        ),
        migrations.AddField(
            model_name='schedule',
            name='posted_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
