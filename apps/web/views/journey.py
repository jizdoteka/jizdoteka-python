from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView
from django.views.generic.edit import FormView
from .. import models
from .. import forms
import googlemaps
from django.contrib import messages
import pudb
from django import http
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


# Create your views here.
# Google API key:  AIzaSyAen5jtHmdJ5ZW3ZOCoqDVjZLkDlILJ014


class WaypointNotFound(Exception):
    pass


class JourneyList(ListView, FormView):
    model = models.Journey
    form_class = forms.SearchJourney
    success_url = reverse_lazy('journey_list')
    filter = {
        'city_from': None, #models.Waypoint.objects.filter(pk=3).get(),
        'city_to': None #models.Waypoint.objects.filter(pk=2).get(),
    }

    GMAPS_CITY_COMPONENT = 'locality'

    def get_context_data(self, **kwargs):
        context = super(JourneyList, self).get_context_data(**kwargs)

        context['form_search_journey'] = forms.SearchJourney()
        context['filter'] = self.filter
        context['is_filter_active'] = self._is_filter_active()

        return context

    def _is_filter_active(self):
        return (self.filter['city_from'] is not None and
                self.filter['city_to'] is not None)

    def __city_to_waypoint_model(self, long_city_name):
        gmaps = googlemaps.Client(key='AIzaSyAen5jtHmdJ5ZW3ZOCoqDVjZLkDlILJ014')

        res = gmaps.geocode(long_city_name)
        if len(res) < 1:
            raise WaypointNotFound(long_city_name)
        res = res[0]
        city = None
        for component in res['address_components']:
            if self.GMAPS_CITY_COMPONENT in component['types']:
                city = component['long_name']
                break

        gps_pos = res['geometry']['location']
        qs = models.Waypoint.objects.filter(
            Q(city=city) | (
                Q(lat=gps_pos['lat']) & Q(long=gps_pos['lng'])
            )
        )
        #print "nalezu v DB=%s, city=%s, zadano=%s, GPS=%s" % (len(qs), city, long_city_name, gps_pos)
        if len(qs) == 0:
            new = models.Waypoint(
                city=city,
                lat=gps_pos['lat'],
                long=gps_pos['lng']
            )
            new.save()
            return new

        return qs.get()

    def form_valid(self, form):
        city_from = self.__city_to_waypoint_model(form.data['city_from'])
        city_to = self.__city_to_waypoint_model(form.data['city_to'])
        self.filter['city_from'] = city_from
        self.filter['city_to'] = city_to
        return super(JourneyList, self).form_valid(form)

    def get_queryset(self):
        if not self._is_filter_active():
            return models.Journey.objects.all()

        # TODO: add other restrictions such as date
        qs = models.Journey.objects.raw('''
            SELECT
                "web_journey".*
            FROM
                "web_journey" LEFT JOIN "web_journeywaypoints" AS "wpt_from" ON ("web_journey"."id" = "wpt_from"."journey_id")
                 LEFT JOIN "web_journeywaypoints" AS "wpt_to" ON ("web_journey"."id" = "wpt_to"."journey_id")
            WHERE
                "wpt_from"."waypoint_id" = '{}'
                AND
                "wpt_to"."waypoint_id" = '{}'
                AND
                "wpt_from"."order" < "wpt_to"."order"
        '''.format(self.filter['city_from'].id, self.filter['city_to'].id)
        )

        #print queryset.filter(
            # 'and' filter by date >= now()
        return qs


class JourneyDetail(DetailView):
    model = models.Journey

    def get_context_data(self, **kwargs):
        context = super(JourneyDetail, self).get_context_data(**kwargs)
        obj = context['object']
        passangers = {}

        class Passanger(object):
            start = None
            _length = 0
            _rest = 0
            _sum = 0
            user = None

            def __init__(self, start, user, sum):
                self.start = start
                self.user = user
                self._sum = sum

            @property
            def length(self):
                return self._length

            @length.setter
            def length(self, val):
                self._length = val
                self._rest = self._sum - self.start - self._length

            @property
            def rest(self):
                return self._sum - self.start - self._length

            def __repr__(self):
                return '%s, start=%s, len=%s' % (self.user, self.start, self.length)

        wpts = obj.journeywaypoints_set
        wpts_count = wpts.count()
        for waypoint in wpts.order_by('order'):
            for p in waypoint.passangers.order_by('-change_timestamp'):
                pobj = passangers.get(
                    p.id,
                    Passanger(start=waypoint.order, user=p, sum=wpts_count))
                pobj.length += 1
                passangers[p.id] = pobj

        context['passangers'] = passangers

        return context


# http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/
class JourneyCreate(CreateView):
    template_name = 'web/journey_create2.html'
    model = models.Journey
    form_class = forms.Journey

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form_wpt = forms.WaypointNewFormSetFactory()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.driver = self.request.user
        form_wpt = forms.WaypointNewFormSetFactory(self.request.POST)

        if form.is_valid() and form_wpt.is_valid():
            return self.form_valid(form, form_wpt)
        else:
            return self.form_invalid(form, form_wpt)

    def form_valid(self, form, form_wpt):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        form_wpt.instance = self.object
        form_wpt.save()

        return HttpResponseRedirect(
            reverse_lazy('journey_detail',
                    kwargs={'pk': self.object.pk}
            )
        )

    def form_invalid(self, form, form_wpt):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt))


class JourneyUpdate(UpdateView):
    template_name = 'web/journey_create2.html'
    model = models.Journey
    form_class = forms.Journey
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """

        super(JourneyUpdate, self).get(request, *args, **kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        qs = models.JourneyWaypoints.objects.filter(
            journey=self.object).order_by('order')

        form_wpt = forms.WaypointUpdateFormSetFactory(
            instance=self.object,
            queryset=qs
        )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                form_wpt=form_wpt,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form_wpt = forms.WaypointUpdateFormSetFactory(self.request.POST,
                                                      instance=self.object)
        #print(form.is_valid(), form_wpt.is_valid())

        if form.is_valid() and form_wpt.is_valid():
            return self.form_valid(form, form_wpt)
        else:
            return self.form_invalid(form, form_wpt)

    def form_valid(self, form, form_wpt):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        form.save()
        form_wpt.save()
        return HttpResponseRedirect(
            reverse_lazy('journey_detail',
                    kwargs={'pk': self.object.pk}
            )
        )

    def form_invalid(self, form, form_wpt):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        super(JourneyUpdate, self).form_invalid(form)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt))


class JourneyDelete(DeleteView):
    model = models.Journey

    def dispatch(self, request, *args, **kwargs):
        obj = models.Car.objects.filter(pk=kwargs['pk']).filter(
            owner=self.request.user)
        if not obj:
            messages.error(request, _('This car is not yours.'))
            return http.HttpResponseRedirect(reverse_lazy('index'))
        messages.info(_('Journey was deleted.'))
        return super(JourneyDelete, self).dispatch(request, *args, **kwargs)