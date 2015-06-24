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

from django.db import models


# This stores all of the scaned URLs from scrapy
class OriginalURL(models.Model):

    # Contains the URL of the post
    url = models.CharField(max_length=1000)

    # Contains the URL of meneame's comments on the post
    meneame_url = models.CharField(max_length=1000)

    # Contains the title of the post, scaned by scrapy
    title = models.CharField(max_length=1000)

    # Contains the date that the post was published on meneame
    pub_date = models.DateField()

    # Contains the hour that the post was published on meneame
    pub_time = models.TimeField()

    # Contains the timestamp date that the post was published on meneame
    pub_date_ts = models.BigIntegerField(null=True)

    # Contains a boolean value indicating if the post went to meneame's front page or not
    frontpage = models.BooleanField(default=False)

    # Contains the date when the post went to meneame's front page
    frontpage_date = models.DateField(null=True)

    # Contains the hour the page went to meneame's front page
    frontpage_time = models.TimeField(null=True)

    # Contains the timestamp date of when the post went to meneame's front page
    frontpage_date_ts = models.BigIntegerField(null=True)

    def __unicode__(self):
        return self.url


# This saves all of the social interactions of the URLs
# NOTE: int stands for interactions, it's too long for a variable
class SocialSync(models.Model):

    # Contains all of the interactions of the post from facebook
    post_facebook_int = models.BigIntegerField(null=True)

    # Contains all of the interactions of the post from twitter
    post_twitter_int = models.BigIntegerField(null=True)

    # Contains the total interactions of the post
    post_total_int = models.BigIntegerField(null=True)

    # Contains the facebook interactions of meneame's comments page
    meneame_facebook_int = models.BigIntegerField(null=True)

    # Contains the twitter interactions of meneame's comments page
    meneame_twitter_int = models.BigIntegerField(null=True)

    # Contains the total interactions of meneame's comments page
    meneame_total_int = models.BigIntegerField(null=True)

    # Contains the date when the social scan was made
    scan_date = models.DateField()

    # Contains the hour when the social scan was made
    scan_time = models.TimeField()

    # Contains the timestamp date of when the social scan was made
    scan_date_ts = models.BigIntegerField(null=True)

    # Contains a foreign key to the OriginalURL entry
    original_url = models.ForeignKey(OriginalURL)

    def __unicode__(self):
        return self.original_url.url


# This model is a way to store all of the errors we might want to store.
# If it's in a model then it's easier to access on user level
class Error(models.Model):

    # This should contain the error message
    error = models.TextField(default="No error defined")

    # This contains who created the error
    created_by = models.CharField(max_length=1000)

    # Contains the date the error was created on
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.error[:15]


# This model is used by social_sync. It's used to store a list of proxies to request
# the Facebook API. This way we are able to bypass the request limit of the API
class FreeProxy(models.Model):

    # The IP of the proxy
    ip = models.CharField(null=False, max_length=255, unique=True)

    # The date the proxy was added
    datetime_added = models.DateTimeField(auto_now_add=True)

    # The last time this proxy was used by the social_sync command
    last_used_datetime = models.DateTimeField(null=True)

    # This is to mark the proxy as obsolete if it doesn't work anymore
    working = models.BooleanField(default=True)

    # This contains the reason the proxy was marked as obsolete
    not_working_reason = models.CharField(null=True, blank=True, max_length=1000)

    def __unicode__(self):
        return self.ip
