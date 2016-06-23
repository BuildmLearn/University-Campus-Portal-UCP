# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_auto_20160618_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discussionthread',
            options={'ordering': ['-posted_at']},
        ),
        migrations.AlterField(
            model_name='attachment',
            name='uploaded_file',
            field=models.ImageField(upload_to=b'user-attachments'),
        ),
    ]
