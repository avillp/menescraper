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

from django.views.generic import TemplateView, ListView
from .models import OriginalURL, SocialSync
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from .forms import SelectDateForm, ListSettingsForm
from django.core.urlresolvers import reverse
import datetime


# This ListView makes a paginated list of all the OriginalURLs
class IndexView(ListView):
    template_name = "web/index.html"

    # How the above queryset will be accesed in the template
    context_object_name = "original_url"

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)

        # Clear all expired sessions
        self.request.session.clear_expired()

        # This checks if the user just changed pages, if it did it stores the page number in a
        # session so it can later be used in the OriginalURLView for the "Go back" button.
        # NOTE: It has to be .GET.get() because if it's just .GET[] django thinks it exists
        # instead if checking if it really exists.
        if self.request.GET.get("page"):
            self.request.session["index_selected_page"] = self.request.GET["page"]

        # If no page is selected it sets the session to nothing because that way it will return
        # to page one. There's an IF inside originalurl.html that will do so.
        else:
            self.request.session["index_selected_page"] = ""

        # This checks if there's a session called listsettings_search
        if self.request.session.get("listsettings_search"):

            # There's a session called as such, that means this user comes from a form, pass
            # the settings that the user selected so there's no need for the user to put them again
            ctx["search"] = self.request.session.get("listsettings_search")

        # Check if any errors got returned for listsettings_error_search
        if self.request.session.get("listsettings_error_search"):
            ctx["listsettings_e1"] = self.request.session.get("listsettings_error_search")

            # Delete the session, it's no longer needed
            del self.request.session["listsettings_error_search"]

        # This checks if there's a session called listsettings_frontpage_only
        if self.request.session.get("listsettings_frontpage_only"):

            # There's a session called as such, that means this user comes from a form, pass
            # the settings that the user selected so there's no need for the user to put them again
            ctx["frontpage_only"] = self.request.session.get("listsettings_frontpage_only")

        # Check if any errors got returned for listsettings_error_frontpage_only
        if self.request.session.get("listsettings_error_frontpage_only"):
            ctx["listsettings_e2"] = self.request.session.get("listsettings_error_frontpage_only")

            # Delete the session, it's no longer needed
            del self.request.session["listsettings_error_frontpage_only"]

        # This checks if there's a session called listsettings_records_per_page
        if self.request.session.get("listsettings_records_per_page"):

            # There's a session called as such, that means this user comes from a form, pass
            # the settings that the user selected so there's no need for the user to put them again
            ctx["records_per_page"] = self.request.session.get("listsettings_records_per_page")

        # Check if any errors got returned for listsettings_error_recxpage
        if self.request.session.get("listsettings_error_recxpage"):
            ctx["listsettings_e3"] = self.request.session.get("listsettings_error_recxpage")

            # Delete the session, it's no longer needed
            del self.request.session["listsettings_error_recxpage"]

        # Passes to the tempate the client address
        ctx["client_address"] = self.request.META.get("REMOTE_ADDR")
        return ctx

    # This is so the user can select the pagination
    def get_paginate_by(self, queryset):

        # Check if the user actually selected a pagination
        if self.request.session.get("listsettings_records_per_page"):

            # The user selected a pagination, set a variable to later on return it
            pagination = self.request.session.get("listsettings_records_per_page")
        else:

            # The user didn't select any pagination, paginate by 10.
            pagination = 10

        # Return the selected pagination
        return pagination

    # This is so the user can filter the objects of the list as desired
    def get_queryset(self):

        # This selects all of the OriginalURLs by default, if the user applied any settings
        # it will be filtered below.
        queryset = OriginalURL.objects.all()

        # Check if the user selected to only show the OriginalURLs on the frontpage
        if self.request.session.get("listsettings_frontpage_only"):

            # The user did so, filter it.
            queryset = queryset.filter(frontpage=True)

        # Check if the user typed in any keywords to follow
        if self.request.session.get("listsettings_search"):

            # The user did so, filter it.
            queryset = queryset.filter(
                title__icontains=self.request.session.get("listsettings_search"))

        # Return the selected objects of OriginalURLs ordering it by publication date
        return queryset.order_by("-pub_date_ts")


class OriginalURLView(TemplateView):
    template_name = "web/originalurl.html"

    def get_context_data(self, **kwargs):
        ctx = super(OriginalURLView, self).get_context_data(**kwargs)

        # This gets the client address to be able to show it on the header
        client_address = self.request.META.get("REMOTE_ADDR")

        try:

            # Tries to get the requested OriginalURL object
            original_url = OriginalURL.objects.get(id=self.kwargs["id"])

        except:

            # Failed to get the requested OriginalURL item, raise 404
            raise Http404("Oops! Item not found.")

        # Gets the current UTC datetime
        current_date = timezone.now()

        # This checks if the user has a the selected_date session set to true,
        # if it does it means that the user used the config form for the chart set to true
        # by the ChangeDateView
        if self.request.session.get("selected_date"):

            # Stores the configured date that is saved in sessions inside the selected_date
            # variable as a datetime.datetime
            selected_date = datetime.date(
                self.request.session.get("selected_date_year"),
                self.request.session.get("selected_date_month"),
                self.request.session.get("selected_date_day"),
            )

        else:

            # The user didn't configure the chart, show the current date of the server
            # It can't contain a time if not it will not work with comparations, we don't need the
            # time anyway
            selected_date = datetime.date(current_date.year, current_date.month, current_date.day)

        # It gets all of the objects from SocialSync that are from the selected date
        social_sync = SocialSync.objects.filter(
            original_url=original_url,
            scan_date=selected_date,
        ).order_by("scan_date")

        # This adds a session to the user saying witch OriginalURL object page the user visited
        # That way the SelectDateView can know which was the last OriginalURL object that the
        # user visited to be able to redirect to it after the form is completed
        self.request.session["original_url_id"] = original_url.id

        # This checks if the user submited a form and it failed
        # It's for the settings form of the chart
        if self.request.session.get("invalid_form"):

            # Because the form failed it gets the error of the session and puts it in a
            # variable, then it removes the session and passes it to the template with ctx
            invalid_form = self.request.session.get("invalid_form")
            del self.request.session["invalid_form"]
            ctx["invalid_form"] = invalid_form

        # This checks if there's a session containing the page the user was on
        # in the IndexView pagination. If there's then it passes it to the template
        # so the "Go back" button goes back to the page the user last was on.
        if self.request.session.get("index_selected_page"):
            ctx["return_url"] = self.request.session.get("index_selected_page")

        # Gets all of the social interactions of the current originalurl and it orders them
        # by the timestamp
        all_social_sync = SocialSync.objects.filter(
            original_url=original_url,
        ).order_by("-scan_date_ts")

        # It checks if it returned any interactions
        if all_social_sync:

            # This gets the last social interaction of the current originalurl and creates a
            # datetime from the timestamp, this is how the "last updated on" message is made.
            ctx["last_social_sync_datetime"] = datetime.datetime.fromtimestamp(
            all_social_sync[0].scan_date_ts)

        # This if it checks if the currently selected date has any interactions and if there's any
        # interactions at all for the selected original_url.
        # By doing this we can take the user to a date that has interactions
        if not social_sync and all_social_sync:

            # Saves the old selected date to be able to tell the user from which date
            # it got switched
            old_selected_date = selected_date

            # This checks if the selected original_url got to the frontpage, if it did, select
            # the frontpage date to show the social interactions of that day
            if original_url.frontpage_date:
                selected_date = original_url.frontpage_date

            # The selected url it's not on the frontpage, select the publication date instead
            else:
                selected_date = original_url.pub_date

            # Queryset to get the social interactions for the selected date
            social_sync = SocialSync.objects.filter(
                original_url=original_url,
                scan_date=selected_date,
            ).order_by("scan_date")

            # Set modified_date to true so the template can know that the selected date got changed
            # and also pass the old selected date so it can tell the user from which date
            # it got switched
            ctx["modified_date"] = True
            ctx["old_selected_date"] = old_selected_date

        # This checks if the URL of the post is actually from facebook. If you request the facebook
        # API with a facebook URL it returns nothing, tell the template to add a message.
        if "facebook" in original_url.url:
            ctx["request_facebook_with_facebook"] = True

        # This checks if the date that is currently selected has any
        # entries to get the y_limit, if not it would crash
        if social_sync:

            # This orders the social_sync by the original_total_int and
            # meneame_total_int that they contain the total of social interactions
            # for the meneame links and normal links and it reverses the order with
            # the - and gets the first one of the list with [0]
            y_limit1 = social_sync.order_by("-post_total_int")[0]
            y_limit2 = social_sync.order_by("-meneame_total_int")[0]

            # Checks if y_limit1 is the one with more interactions or not to then
            # add a 20% to it so the graph shows a 20% more
            if y_limit1.post_total_int > y_limit2.meneame_total_int:
                y_limit = y_limit1.post_total_int
                y_limit += y_limit1.post_total_int * 0.20

            else:
                y_limit = y_limit2.meneame_total_int
                y_limit += y_limit2.meneame_total_int * 0.20

        else:
            y_limit = 0

        # READ BEFORE ADDING CODE BELOW:
            # all the part that selects the Y limits of the chart is important that it stays
            # below the queryset that will select the social interactions. If it first gets the
            # chart limits based on the selected social interactions and then it actually
            # selects the social interactions it will not work for obvious reasons

        # This IF tells the template if it has to show the frontpage date line or not
        # This selects true if the date that the user selected is the date that the post went to
        # the frontpage. This is to avoid the chart breaking.
        if original_url.frontpage_date == selected_date:
            frontpage_chartline = True
        else:
            frontpage_chartline = False

        # This gets the timestamp date of when the post went to the frontpage.
        # Then it assings a variable containing the height of the chart +1 so the dot
        # of the frontpage will be off the chart so only a line shows up
        frontpage_ts = original_url.frontpage_date_ts
        frontpage_yrange = y_limit + 1

        # Puts everything in ctx to then return it for the template to use it
        ctx["frontpage_chartline"] = frontpage_chartline
        ctx["selected_date"] = selected_date
        ctx["frontpage_ts"] = frontpage_ts
        ctx["frontpage_yrange"] = frontpage_yrange
        ctx["current_date"] = current_date
        ctx["y_limit"] = y_limit
        ctx["social_int"] = social_sync
        ctx["client_address"] = client_address
        ctx["original_url"] = original_url
        return ctx


def ChangeDateView(request):

    # It checks if the method used is POST
    if request.method == "POST":

        # Creates a form with the POST information received
        form = SelectDateForm(request.POST)

        # Checks if the sent form is valid
        if form.is_valid():

            # It stores in different sessions the day month and year submited by the user in the
            # form. It has to be stored in session separated because sessions can't save JSONs
            request.session["selected_date_day"] = form.cleaned_data["date"].day
            request.session["selected_date_month"] = form.cleaned_data["date"].month
            request.session["selected_date_year"] = form.cleaned_data["date"].year

            # Set the sessions to expire in 2 hours
            request.session.set_expiry(7200)

            # This session is for OriginalURLView, so it can check if the user submited a form
            request.session["selected_date"] = True

            # It returns to the OriginalURL object page with the ID given by OriginalURLView
            return HttpResponseRedirect(reverse("original_url",
                kwargs={
                    "id": request.session.get("original_url_id"),
                    }))
        else:

            # It stores the error of the form in a session so it can be displayed to the user
            request.session["invalid_form"] = str(form.errors["date"])

            # Goes back to the OriginalURLView
            return HttpResponseRedirect(reverse("original_url",
                kwargs={
                    "id": request.session.get("original_url_id"),
                    }))

    # If the request method is not POST it raises 404
    raise Http404


# This is the view that processes the settings form of the index list
def ListSettingsView(request):

    # This checks if the request is actually comming from a form using post
    if request.method == "POST":

        # Create a form object with the received form via post
        form = ListSettingsForm(request.POST)

        # Check if there's any errors with the form
        if form.is_valid():

            # This puts in sessions what was inside the form fields so IndexView can do it's thing.
            request.session["listsettings_search"] = form.cleaned_data["search"]
            request.session["listsettings_frontpage_only"] = form.cleaned_data["frontpage_only"]
            request.session["listsettings_records_per_page"] = form.cleaned_data["records_per_page"]

            # Set the sessions to expire in 2 hours
            request.session.set_expiry(7200)

        # It executes if the form contains errors, process the errors.
        else:

            # Checks if the search field is the one having problems
            if form.has_error("search"):

                # Pass the error message
                request.session["listsettings_error_search"] = str(form.errors["search"])

            # Checks if the frontpage_only field is the one having problems
            if form.has_error("frontpage_only"):

                # Pass the error message
                request.session["listsettings_error_frontpage_only"] = str(
                    form.errors["frontpage_only"])

            # Checks if the records_per_page field is the one having problems
            if form.has_error("records_per_page"):

                # Pass the error message
                request.session["listsettings_error_recxpage"] = str(
                    form.errors["records_per_page"])

        # Redirect the user to index
        return HttpResponseRedirect(reverse("index"))

    # Raise 404 because the request doesn't come from a form
    raise Http404