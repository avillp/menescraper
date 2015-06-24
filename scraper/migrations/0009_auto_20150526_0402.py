# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_auto_20150526_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeproxy',
            name='ip',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
