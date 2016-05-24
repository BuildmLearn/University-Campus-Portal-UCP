# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20160524_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailvericationcode',
            name='expiry_date',
            field=models.DateField(),
        ),
    ]
