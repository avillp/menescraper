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

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class URLItem(scrapy.Item):
    url = scrapy.Field()
    meneame_url = scrapy.Field()
    title = scrapy.Field()
    pub_date = scrapy.Field()
    pub_time = scrapy.Field()
    pub_date_ts = scrapy.Field()
    frontpage = scrapy.Field()
    frontpage_date = scrapy.Field()
    frontpage_time = scrapy.Field()
    frontpage_date_ts = scrapy.Field()