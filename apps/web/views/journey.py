rom django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, RedirectView, CreateView
from django.views.generic.edit import FormView
from . import models
from . import forms
import googlemaps
from pprint import pprint
import pudb
from django.db.models import Q


# Create your views here.
# Google API key:  AIzaSyAen5jtHmdJ5ZW3ZOCoqDVjZLkDlILJ014


class WaypointNotFound(Exception):
    pass


class JourneyList(ListView, FormView):
    model = models.Journey
    form_class = forms.SearchJourney
    success_url = '/'   # TODO: replace by generic URL of this page
    filter = {
        'city_from': models.Waypoint.objects.filter(pk=4).get(),
        'city_to': models.Waypoint.objects.filter(pk=1).get(),
    }

    GMAPS_CITY_COMPONENT = 'locality'

    def get_initial(self):
        initial = super(JourneyList, self).get_initial()
        #filter = {
        #    'city_from': self.filter['city_from'].city,
        #    'city_to': self.filter['city_to'].city,
        #}
        #initial.update(filter)
        return initial

    def get_context_data(self, **kwargs):
        context = super(JourneyList, self).get_context_data(**kwargs)

        context['form_search_journey'] = forms.SearchJourney()
        context['filter'] = self.filter
        context['filter_from'] = self.filter['city_from']
        context['filter_to'] = self.filter['city_to']

        return context

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
        city_from = self.__city_to_waypoint_model(form.data['city_from']).id
        city_to = self.__city_to_waypoint_model(form.data['city_to']).id
        self.filter['city_from'] = city_from
        self.filter['city_to'] = city_to
        return super(JourneyList, self).form_valid(form)

    def get_queryset(self):
        # queryset = super(JourneyList, self).get_queryset()
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
        '''.format(self.filter['city_from'], self.filter['city_to'])
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
            for p in waypoint.passangers.all():
                pobj = passangers.get(
                    p.id,
                    Passanger(start=waypoint.order, user=p, sum=wpts_count))
                pobj.length += 1
                passangers[p.id] = pobj

        context['passangers'] = passangers

        return context

