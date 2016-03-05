from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, RedirectView

# FIXME: Really, really ugly!
from .. import models


class JourneyList(ListView):
    model = models.Journey


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

