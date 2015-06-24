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
from django import forms


# This form is in originalurl and it's so the user can select the date of the graph
class SelectDateForm(forms.Form):

    # Contains the selected date
    date = forms.DateField()


# This form is to allow the user customize how he sees the list in index
class ListSettingsForm(forms.Form):

    # Contains the keywords the user entered
    search = forms.CharField(required=False)

    # Contains a boolean. True to show only the frontpage posts and False to show
    # everything
    frontpage_only = forms.BooleanField(required=False)

    # The number of records to show per page
    records_per_page = forms.IntegerField()