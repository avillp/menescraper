'''
MeneScraper is a big data project that monitors the social interactions of Meneame.
Copyright (C) 2015  Arnau Villoslada

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# This two lines allow this file to use models
import django
django.setup()

from scraper.models import OriginalURL


class MeneamePipeline(object):

    # This processes the item when received, item contains the item and spider contains the spider
    # that was executed
    def process_item(self, item, spider):

        # This checks if the item that was scanned it's not in frontpage
        if not item["frontpage"]:

            # This creates the new OriginalURL object if it doesn't exist
            OriginalURL.objects.get_or_create(
                url=item["url"],
                meneame_url=item["meneame_url"],
                title=item["title"],
                pub_date=item["pub_date"],
                pub_time=item["pub_time"],
                pub_date_ts=item["pub_date_ts"],
                frontpage=item["frontpage"],
            )

        # This checks if the item that was scanned it's from the frontpage
        elif item["frontpage"]:

            # This tries to find the item in the OriginalURL model
            try:
                original_url_model = OriginalURL.objects.get(url=item["url"], frontpage=False)

            # If it doesn't exist it just ignores it because we don't want links that were not in
            # frontpage before
            except OriginalURL.DoesNotExist:
                pass

            # This executes when the link was found in the module and it updates it to add
            # the check of frontpage and adds the date of when it went to frontpage
            else:
                original_url_model.frontpage = item["frontpage"]
                original_url_model.frontpage_date = item["frontpage_date"]
                original_url_model.frontpage_time = item["frontpage_time"]
                original_url_model.frontpage_date_ts = item["frontpage_date_ts"]
                original_url_model.save()

        return item
