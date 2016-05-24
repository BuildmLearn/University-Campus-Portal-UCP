# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0003_auto_20160524_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVericationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('verification_code', models.CharField(max_length=100, blank=True)),
                ('expiry_date', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailvericationcodes',
            name='user',
        ),
        migrations.DeleteModel(
            name='EmailVericationCodes',
        ),
    ]
