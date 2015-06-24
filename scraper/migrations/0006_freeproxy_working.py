# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20150526_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeproxy',
            name='working',
            field=models.BooleanField(default=True),
        ),
    ]
