# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20150525_2258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freeproxy',
            old_name='date_added',
            new_name='datetime_added',
        ),
        migrations.RenameField(
            model_name='freeproxy',
            old_name='last_used',
            new_name='last_used_datetime',
        ),
    ]
