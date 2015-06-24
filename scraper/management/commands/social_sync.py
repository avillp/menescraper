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

# Imports
from django.core.management.base import BaseCommand
from scraper.models import SocialSync, OriginalURL, Error, FreeProxy
from django.utils import timezone
from random import randint
# I know this can be done on one line like: urllib, json... but NINJA-IDE doesn't let me
import urllib
import json
import time
import socket
import datetime


# When called, it checks the twitter interactions of the given URL.
# If successful it returns the interactions returned by the twitter API
# If it fails, returns false.
def TwitterScan(encoded_url):

    # This tries to request the api, if successful extract the json
    try:
        twitter_req = urllib.urlopen(
            "http://urls.api.twitter.com/1/urls/count.json?url={url}".format(url=encoded_url)
        )

    # Exception occured with urllib.urlopen(), store it in the Error model
    except Exception as e:

        error = Error(
            error="URL: {url}\nTwitter API error: {error}".format(
                error=e,
                url=encoded_url,
            ),
            created_by="social_sync.py",
        )
        error.save()

        # Print that it failed
        print " This one failed! Automatically saved in errors model"

        # Return False so the Command function can know it failed.
        return False

    # Successfully requested the API, transform to JSON and return the total interactions
    twitter_json = json.load(twitter_req)
    return twitter_json["count"]


# When called, it tries to visit the Facebook API with the given URL to extract the
# total social interactions. If succesful it returns the total interactions,
# otherwhise, returns False.
def FacebookScan(encoded_url, use_proxies):

    # This checks if the user said that it wants to sync using proxies
    if use_proxies:
        # This assings the maximum time in seconds to wait for the urllib.urlopen() below to
        # respond
        socket.setdefaulttimeout(15)

        # This gets the proxy that was used longer ago from the FreeProxy model.
        # It also returns the proxy IP in a dictionary to use with urllib.urlopen
        oldest_proxy, oldest_proxy_dic = OldestProxyDic()

        # The function to get the proxies failed, without proxies this function can't continue
        # return false.
        if oldest_proxy is False:
            return False

    # If this runs it means the user didn't select any proxy.
    # Just assign an empty dictionary, that way urllib.openurl() will ignore the proxies
    # argument and use localhost
    else:
        oldest_proxy_dic = {"": ""}

    # We have to use this because if the URL contains things like "?X=" the facebook API
    # will think we are passing parameters to it.
    encoded_url = urllib.quote(encoded_url)

    # This tries to request the Facebook API. If successful, it will extract the JSON.
    # If it fails it will return False to let the Command function know it did so.
    try:

        # IMPORTANT NOTE: The idea to use proxies was to bypass the API request limit.
        # If we are using proxies + an access_token, it makes no sense to use proxies but
        # for now we have to use an access_token until a new function is coded for the proxies.
        # The reason for that is, the facebook API json changes when you visit it without an
        # access token, that means the json is different and so a new function is required.
        facebook_req = urllib.urlopen(
            "https://graph.facebook.com/v2.3/{url}?access_token="
            "CONFIGURE-ME: Add the your Facebook access token".format(url=encoded_url),
            proxies=oldest_proxy_dic,
        )

    # The urllib.urlopen() returned an exception, store it in the Error model
    except Exception as e:

        error = Error(
            error="URL: {url}\nurllib.urlopen() error: {error}".format(
                error=e,
                url=encoded_url,
            ),
            created_by="social_sync.py",
        )
        error.save()

        # This checks if the exception was caused for any of the following reasons
        # If it did, call the DisableProxy function to mark the used proxy as obsolete.
        if "[Errno socket error]" in str(e) or "http protocol error" in str(e):
            DisableProxy(oldest_proxy, e)

        # Tell the user it failed
        print " This one failed! Automatically saved in errors model"

        # Return false instead of the social interactions
        return False

    # This checks if the returned html is actually a json. If it's not json, the proxy works,
    # if it isn't, the proxy is obsolete
    try:
        facebook_json = json.load(facebook_req)

    except Exception as e:

        error = Error(
            error=(
                "URL: {url}\n"
                "json.load() error: {error}\n"
                "Proxy used during error: {proxy_ip}"
                ).format(
                    error=e,
                    url=encoded_url,
                    proxy_ip=oldest_proxy.ip,
                ),
            created_by="social_sync.py",
        )
        error.save()

        # This proxy is obsolete, call DisableProxy to mark it as such in the FreeProxy model
        DisableProxy(oldest_proxy, e)

        # Tell the user it failed
        print " This one failed! Automatically saved in errors model"

        # Tell the Command function it failed
        return False

    # This checks if there's a key called error in the facebook json.
    # If so, the facebook api returned an error.
    if "error" in facebook_json:

        # Tell the user the API returned an exception and the exception message
        print " Facebook API returned exception:"
        print "  {exception}".format(exception=facebook_json["error"]["message"])

        # Store the error in the Error model
        error = Error(
            error="URL: {url}\nFacebook API returned exception:\n{error}".format(
                error=facebook_json["error"]["message"],
                url=encoded_url,
            ),
            created_by="social_sync.py",
        )
        error.save()

        # Return False instead of the total interactions
        return False

    # Everything went fine; return the total interactions
    return facebook_json["share"]["share_count"]


# This function is used to select the best proxy to use to request the API
# If it fails, it returns false
def OldestProxyDic():

    # This queryset ignores any proxy marked as obsolete and orders them by used date
    oldest_proxy = FreeProxy.objects.filter(working=True).order_by("last_used_datetime")

    # This counts how many results the above query returned
    proxies_count = oldest_proxy.count()

    # This part will choose randomly one of 4 proxies at the start of the queryset.
    # This way there will be no pattern in the proxies we use and the ones that were used
    # longer ago will be used now.
    # No pattern = harder to detect by a machine and block it.
    if proxies_count > 3:

        # There's more than 4 proxies available in the list, randomly choose between 0 and 3
        random_int = randint(0, 3)
    elif proxies_count == 1:

        # There is only one proxy available, select that one
        random_int = 0

        # Tell the user there's only one proxy left
        print " WARNING: Only one proxy is available"

    # Check if the FreeProxy model has proxies at all
    elif proxies_count == 0:

        # No proxies left, tell the user and return false so the FacebookScan
        # function knows it failed
        print " Error: No proxies found, please add more."
        return (False, False)

    else:
        random_int = randint(0, proxies_count)

    # It gets the proxy selected randomly by the above if and else. This way we avoid
    # creating a loop. If there's no loop, there's no pattern = harder to detect by
    # a machine and block it.
    oldest_proxy = oldest_proxy[random_int]

    # It generates the dicctionary needed for the urllib.urlopen() so the FacebookScan function
    # doesn't need to do it
    oldest_proxy_dic = {"http": "http://" + oldest_proxy.ip}

    # Saves the the last time the proxy we just selected was last used, witch is right now.
    oldest_proxy.last_used_datetime = timezone.now()
    oldest_proxy.save()

    # Return the proxy and the dictonary we just got
    return (oldest_proxy, oldest_proxy_dic)


# This is needed to mark the proxies as obsoletes if needed and to respect the DRY rule.
# You can check why we might want to mark a proxy as obsolete in the FacebookScan function.
def DisableProxy(free_proxy, reason):
    free_proxy.working = False
    free_proxy.not_working_reason = reason
    free_proxy.save()
    print " Marked {proxy_ip} as obsolete".format(proxy_ip=free_proxy.ip)


class Command(BaseCommand):

    # Just some help text for the ./manage.py help social_sync command
    # These comments(lint) are so Ninja-IDE ignores this line so it wont display errors
    #lint:disable
    help = "Get the Twitter and Facebook social interactions of all the links in the database"
    #lint:enable

    def add_arguments(self, parser):

        # This is to define the argument --use-proxies. This way the user can select if
        # he wants to use proxies or not to request the Facebook API
        parser.add_argument("--use-proxies",
            action="store_true",
            dest="use_proxies",
            default=False,
            help="Use proxies to request the Facebook API",
        )

        # This is a required argument. With --days-back the user can choose how many days
        # back wants to sync from the OriginalURL model
        parser.add_argument("--days-back",
            action="store",
            dest="days_back",
            default=False,
            help="Define with an integer how many days back you want to sync\n"
                "Example: Current date is 2015-30-05.\n"
                "        'social_sync --days-back 0,1' would sync days 30 and 29",
        )

    def handle(self, *args, **options):

        # Checks if the user used the days-back argument, witch is required
        if not options["days_back"]:

            # Tell the user the days-back argument is required
            return "Please define how many days back you want to sync with '--days-back'"

        # Make a list of the string given by the user. Expect a list created with commas
        days_back = options["days_back"].split(",")

        # This checks if what the user gave us two objects.
        # If the user doesn't separate the numbers with a comma, this will also triger
        # because the .split(",") only separates from the commas
        if len(days_back) != 2:
            return "Please use only two integers separated by a comma. EX: 0,4"

        # Tries to convert what to user gave us with the days-back argument to an integer
        try:

            # Convert the strings the user gave us to integers
            days_back[0] = int(days_back[0])
            days_back[1] = int(days_back[1])

        # This executes when the user doesn't use integers
        except:

            # Tell the user that the days-back argument only works with integers
            return "Please use integers only with --days-back"

        # Sort the integers the user gave us, this has to be done because the user
        # could type the integers in reverse order by accident EX: 4,1
        days_back = sorted(days_back)

        # This gets the current date and time and it saves the date in current_date
        # excluding the time, we don't need that
        rightnow = timezone.now()
        current_date = datetime.date(rightnow.year, rightnow.month, rightnow.day)

        # From the current date it extracts X days to get the two neccesary variables
        # for the queryset. X is defined by the user
        from_date = current_date - datetime.timedelta(days=days_back[1])
        to_date = current_date - datetime.timedelta(days=days_back[0])

        # Gets the objects from the date the user told us and loops them
        original_url = OriginalURL.objects.filter(pub_date__range=(from_date, to_date))

        if not original_url.count():
                return "No {days} days old entries found".format(days=days_back)

        for url in original_url:

            # Gets the url of the current object and encodes it to utf-8 to avoid crashes
            actual_url = url.url.encode("utf-8")

            # Tell the user witch url is processing
            print "Processing {url}".format(url=actual_url)

            # This calls the FacebookScan function to get the facebook interactions of the
            # post URL
            facebook_int = FacebookScan(actual_url, options["use_proxies"])

            # This calls the TwitterScan function to get the twitter interactions of the
            # post URL
            twitter_int = TwitterScan(actual_url)

            # If any of those functions returns false it means something went wrong, go
            # to the next OriginalURL
            if facebook_int is False or twitter_int is False:
                continue

            # Add the total interactions of facebook and twitter to get the total.
            total_int = int(facebook_int + twitter_int)

            # This creates a new object in the SocialSync model to save all the info that
            # we just got and links this object with the right OriginalURL object
            social_sync = SocialSync(
                post_facebook_int=facebook_int,
                post_twitter_int=twitter_int,
                post_total_int=total_int,
                scan_date=timezone.now(),
                scan_time=timezone.now(),
                scan_date_ts=int(time.mktime(timezone.localtime(
                    timezone.now()).timetuple())),
                original_url=url,
            )
            social_sync.save()

            # Some messages for the user, it doesn't hurt
            print " Added {facebook_int} Facebook interacitons".format(
                facebook_int=facebook_int)

            print " Added {twitter_int} Twitter interactions".format(
                twitter_int=twitter_int)

            print " Scan date: {now}".format(
                now=timezone.localtime(timezone.now()))

            print " Total URL interactions: {total_int}".format(
                total_int=total_int)

            # Let's now add the Meneame URL interactions
            meneame_url = url.meneame_url.encode("utf-8")

            # This calls the FacebookScan function to get the facebook interactions of the
            # meneame URL
            facebook_int = FacebookScan(meneame_url, options["use_proxies"])

            # This calls the TwitterScan function to get the twitter interactions of the
            # meneame URL
            twitter_int = TwitterScan(meneame_url)

            # If any of those functions returns false it means something went wrong, go
            # to the next OriginalURL
            if facebook_int is False or twitter_int is False:
                if social_sync:
                    social_sync.delete()
                    print " Entry deleted due to a failure"
                continue

            # Add the total interactions of facebook and twitter to get the total.
            total_int = int(facebook_int + twitter_int)

            # If this executes it's because everything went just fine, so it adds them
            social_sync.meneame_facebook_int = facebook_int
            social_sync.meneame_twitter_int = twitter_int
            social_sync.meneame_total_int = total_int
            social_sync.save()

            # Let's tell the user that we are done and everything went just fine and the
            # total of interactions made
            print " Total Meneame interactions: {total_int}".format(total_int=total_int)
            print " Completed successfully"