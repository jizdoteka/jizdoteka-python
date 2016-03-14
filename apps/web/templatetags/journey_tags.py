from django import template
import re

register = template.Library()

@register.filter
def first_city(queryset):
    return queryset.order_by('order')[0].waypoint


@register.filter
def first_city_id(queryset):
    return queryset.order_by('order')[0].waypoint.id


@register.filter
def last_city(queryset):
    return queryset.order_by('-order')[0].waypoint

@register.filter
def last_city_id(queryset):
    return queryset.order_by('-order')[0].waypoint.id

@register.filter
def sort_wpts(queryset):
    return queryset.order_by('order')


@register.filter
def pretty_name(queryset):
    return '%s %s [%s]' % (
        queryset.first_name,
        queryset.last_name,
        queryset.username
    )


@register.simple_tag
def count_free_seats(journey, wpt_from, wpt_to):
    free_seats = []
    inside = False
    for wpt in journey.journeywaypoints_set.order_by('order'):
        if wpt.waypoint.id == wpt_from.id:
            inside = True
        if wpt.waypoint.id == wpt_to.id:
            inside = False
        if inside:
            seats = wpt.free_seats()
            if seats == 0:
                return seats
            free_seats.append(seats)
    return min(free_seats)


@register.filter
def num_free_seats(wpt, city_from, city_to):
    return wpt.free_seats(city_from, city_to)


@register.filter
def wpt_passangers_order(wpt):
    return wpt.passangers.order_by('-change_timestamp')


@register.filter
def get_range(value):
    """
    https://djangosnippets.org/snippets/1357/
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)
