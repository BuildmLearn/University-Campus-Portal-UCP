# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20160529_0607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uploaded_file', models.FileField(upload_to=b'/user-attachments/')),
                ('size', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('posted_at', models.DateField()),
                ('no_of_replies', models.IntegerField(null=True, blank=True)),
                ('no_of_views', models.IntegerField(null=True, blank=True)),
                ('posted_by', models.ForeignKey(to='login.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posted_at', models.DateField()),
                ('text', models.CharField(max_length=b'1000', null=True)),
                ('posted_by', models.ForeignKey(to='login.UserProfile')),
                ('thread', models.ForeignKey(to='discussion.DiscussionThread')),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='reply',
            field=models.ForeignKey(to='discussion.Reply'),
        ),
    ]
