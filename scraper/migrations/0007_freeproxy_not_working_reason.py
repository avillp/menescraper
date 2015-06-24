# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_freeproxy_working'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeproxy',
            name='not_working_reason',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
