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

from django.contrib import admin
from .models import *


# Tabularinlines
class SocialSyncAdminInline(admin.TabularInline):
    model = SocialSync
    extra = 0

    readonly_fields = (
        "post_facebook_int",
        "post_twitter_int",
        "post_total_int",
        "meneame_facebook_int",
        "meneame_twitter_int",
        "meneame_total_int",
        "scan_date",
        "scan_time",
        "scan_date_ts",
        "original_url",
    )


# ModelAdmins
class OriginalURLAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "url",
        "frontpage",
        "pub_date",
        "pub_time",
        "pub_date_ts",
        "frontpage_date",
        "frontpage_time",
        "frontpage_date_ts",
    )

    search_fields = (
        "id",
        "url",
        "title",
        "meneame_url",
    )

    list_filter = (
        "pub_date",
        "frontpage_date",
        "frontpage",
    )

    fields = (
        "url",
        "meneame_url",
        "title",
        "pub_date",
        "pub_time",
        "pub_date_ts",
        "frontpage_date",
        "frontpage_time",
        "frontpage_date_ts",
        "frontpage",
    )

    readonly_fields = (
        "url",
        "meneame_url",
        "title",
        "pub_date",
        "pub_time",
        "pub_date_ts",
        "frontpage",
        "frontpage_date",
        "frontpage_time",
        "frontpage_date_ts",
    )

    inlines = [
        SocialSyncAdminInline,
    ]

admin.site.register(OriginalURL, OriginalURLAdmin)


class SocialSyncAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post_facebook_int",
        "post_twitter_int",
        "post_total_int",
        "meneame_facebook_int",
        "meneame_twitter_int",
        "meneame_total_int",
        "scan_date",
        "original_url",
    )

    list_filter = (
        "scan_date",
    )
    readonly_fields = (
        "post_facebook_int",
        "post_twitter_int",
        "post_total_int",
        "meneame_facebook_int",
        "meneame_twitter_int",
        "meneame_total_int",
        "scan_date",
        "scan_time",
        "scan_date_ts",
        "original_url",
    )


admin.site.register(SocialSync, SocialSyncAdmin)


class ErrorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_by",
        "created_on",
    )

    list_filter = (
        "created_on",
    )

    readonly_fields = (
        "created_by",
        "created_on",
    )

    fields = (
        "created_by",
        "created_on",
        "error",
    )

    search_fields = (
        "error",
        "created_on",
        "created_by",
        "id",
    )

admin.site.register(Error, ErrorAdmin)


class FreeProxyAdmin(admin.ModelAdmin):

    list_display = (
    "id",
    "ip",
    "datetime_added",
    "last_used_datetime",
    "working",
    )

admin.site.register(FreeProxy, FreeProxyAdmin)