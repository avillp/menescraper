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

import scrapy
from meneame.items import URLItem
import datetime


class MeneameSpider(scrapy.Spider):

    # The name of the spider
    name = "meneame"

    # Self explanatory
    allowed_domains = [
        "meneame.net",
    ]

    # The first urls that will get crawled, I say first because scrapy has the option
    # to follow links
    start_urls = [
        "https://www.meneame.net/queue?meta=_popular",
        "https://www.meneame.net",
    ]

    def parse(self, response):

        # If the url for example is "https://www.meneame.net/queue?meta=_popular" this will split
        # the url in a list. It will split the url from the / of it and get the -1 item from the
        # list "queue?meta=_popular"
        page = response.url.split("/")[-1]

        # This if checks if what it's parsing it's from the queue page
        if page == "queue?meta=_popular":

            # This loops all of the divs in the queue page
            for sel in response.xpath("//div"):

                # This checks if the looped div contains an <h2> and an <a.. inside
                if sel.xpath("h2/a"):

                    # Creates scrapy item in a variable
                    url_item = URLItem()

                    # Gets the URL of the post
                    url = sel.xpath("h2/a/@href").extract()[0]
                    url_item["url"] = url

                    # Gets the title of the post
                    url_item["title"] = sel.xpath("h2/a/text()").extract()[0]

                    # Gets the publication date timestamp and converts it to datetime
                    pub_date = int(
                        sel.xpath("div/span[@class='ts visible']/@data-ts").extract()[0])
                    url_item["pub_date"] = datetime.datetime.fromtimestamp(
                        pub_date).date()

                    # This transforms the date from timestamp to datetime and extracts the time
                    pub_time = datetime.datetime.fromtimestamp(
                        pub_date).time()
                    url_item["pub_time"] = pub_time

                    # Puts the publication date timestamp that we got before into the scrapy item
                    url_item["pub_date_ts"] = pub_date

                    # This is used later on to check if the URLs are on the frontpage or not
                    url_item["frontpage"] = False

                    # This scraps the url of the meame commnets, the problem is that the urls
                    # don't contain the https://www.meneame.net part, so it has to be added
                    url = "https://www.meneame.net" + sel.xpath(
                        "div/span[@class='comments-counter']/a/@href").extract()[0]
                    url_item["meneame_url"] = url

                    # Call pipeline to process all of the data that we got
                    itemproc = self.crawler.engine.scraper.itemproc
                    itemproc.process_item(url_item, self)

        # This checks if the URL that is parsing it's the frontpage
        elif page == "www.meneame.net":

            # This loops all of the divs in the queue page
            for sel in response.xpath("//div"):

                # This checks if the looped div contains an <h2> and an <a.. inside
                if sel.xpath("h2/a"):

                    # Creates scrapy item in a variable
                    url_item = URLItem()

                    # The news in frontpage have 2 data-ts. One for the publication date and another
                    # that says when it went to frontpage. Because of the order that they are in the
                    # HTML the publication date goes first: [0] and the frontpage date
                    #  goes second: [1]
                    frontpage_date = int(
                        sel.xpath("div/span[@class='ts visible']/@data-ts").extract()[1])

                    # Gets the URL of the post
                    url = sel.xpath("h2/a/@href").extract()[0]
                    url_item["url"] = url

                    # Gets the title of the post
                    url_item["title"] = sel.xpath("h2/a/text()").extract()[0]

                    # This is used later on to check if the URLs are on the frontpage or not
                    url_item["frontpage"] = True

                    # This gets the date of when it got to the frontpage in timestamp and turns it
                    # to a datetime
                    url_item["frontpage_date"] = datetime.datetime.fromtimestamp(
                        frontpage_date).date()

                    # This transforms the date from timestamp to datetime and extracts the time
                    frontpage_time = datetime.datetime.fromtimestamp(
                        frontpage_date).time()
                    url_item["frontpage_time"] = frontpage_time

                    # It's multiplied by 1000 so it's compatible with the scan_date_ts
                    # from the SocialSync model
                    url_item["frontpage_date_ts"] = frontpage_date

                    # This scraps the url of the meame commnets, the problem is that the urls
                    # don't contain the https://www.meneame.net part, so it has to be added
                    url = "https://www.meneame.net" + sel.xpath(
                        "div/span[@class='comments-counter']/a/@href").extract()[0]
                    url_item["meneame_url"] = url

                    # Call pipeline to process all of the data that we got
                    itemproc = self.crawler.engine.scraper.itemproc
                    itemproc.process_item(url_item, self)

        # On the last commit I uploaded a settings.pyc by accident, ignore it for the next commit