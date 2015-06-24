# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_freeproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeproxy',
            name='last_used',
            field=models.DateTimeField(null=True),
        ),
    ]
