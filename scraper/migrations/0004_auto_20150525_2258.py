# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_auto_20150525_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeproxy',
            name='ip',
            field=models.CharField(max_length=1000),
        ),
    ]
