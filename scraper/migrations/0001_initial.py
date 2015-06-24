# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('error', models.TextField(default=b'No error defined')),
                ('created_by', models.CharField(max_length=1000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OriginalURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=1000)),
                ('meneame_url', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=1000)),
                ('pub_date', models.DateField()),
                ('pub_time', models.TimeField()),
                ('pub_date_ts', models.BigIntegerField(null=True)),
                ('frontpage', models.BooleanField(default=False)),
                ('frontpage_date', models.DateField(null=True)),
                ('frontpage_time', models.TimeField(null=True)),
                ('frontpage_date_ts', models.BigIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialSync',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_facebook_int', models.BigIntegerField(null=True)),
                ('post_twitter_int', models.BigIntegerField(null=True)),
                ('post_total_int', models.BigIntegerField(null=True)),
                ('meneame_facebook_int', models.BigIntegerField(null=True)),
                ('meneame_twitter_int', models.BigIntegerField(null=True)),
                ('meneame_total_int', models.BigIntegerField(null=True)),
                ('scan_date', models.DateField()),
                ('scan_time', models.TimeField()),
                ('scan_date_ts', models.BigIntegerField(null=True)),
                ('original_url', models.ForeignKey(to='scraper.OriginalURL')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
