# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_auto_20160703_0413'),
        ('login', '0018_userprofile_is_moderator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result_file', models.FileField(upload_to=b'result_files')),
                ('title', models.CharField(max_length=100, blank=True)),
                ('tags', models.ManyToManyField(to='discussion.Tag')),
                ('teacher', models.ForeignKey(to='login.UserProfile')),
            ],
        ),
    ]
