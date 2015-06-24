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

from django.conf.urls import patterns, include, url
from django.contrib import admin
from scraper import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'menescraper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^(?P<id>[0-9]+)/$", views.OriginalURLView.as_view(), name="original_url"),
    url(r"^changedate/$", views.ChangeDateView, name="change_date"),
    url(r"^changesettings/$", views.ListSettingsView, name="change_settings"),
)
