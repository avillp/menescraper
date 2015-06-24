# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0009_auto_20150526_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeproxy',
            name='datetime_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
