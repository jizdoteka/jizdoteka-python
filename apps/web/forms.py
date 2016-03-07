from django import forms
from . import models


class SearchJourney(forms.Form):
    city_from = forms.CharField()
    city_to = forms.CharField()


class Journey(forms.ModelForm):
    class Meta:
        model = models.Journey
        fields = ['seats', 'driver', 'date', 'approx', 'approx_note', 'currency']


wpt_base_factory_kwargs = {
    'parent_model': models.Journey,
    'model': models.JourneyWaypoints,
    'fields': ('waypoint', 'order', 'label', 'output_only', 'segment_price'),
    'extra': 0,
    'can_order': True,
    'can_delete': True,
}
wpt_new_factory_kwargs = dict(wpt_base_factory_kwargs)
wpt_update_factory_kwargs = dict(wpt_base_factory_kwargs)
wpt_new_factory_kwargs['extra'] = 2

WaypointNewFormSetFactory = forms.inlineformset_factory(
    **wpt_new_factory_kwargs)
WaypointUpdateFormSetFactory = forms.inlineformset_factory(
    **wpt_update_factory_kwargs)


class JourneyFormSet(forms.ModelForm):
    class Meta:
        model = models.JourneyWaypoints
        fields = ['journey', 'waypoint', 'label']
        js = ('js/jquery.js',)
