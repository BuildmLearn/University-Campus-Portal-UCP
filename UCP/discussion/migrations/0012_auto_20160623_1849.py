# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0011_attachment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='reply',
            field=models.ForeignKey(related_name='attachments', to='discussion.Reply'),
        ),
    ]
