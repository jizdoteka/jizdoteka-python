from django import forms
from . import models


class SearchJourney(forms.Form):
    city_from = forms.CharField()
    city_to = forms.CharField()


class Journey(forms.ModelForm):
    class Meta:
        model = models.Journey
        fields = ['seats', 'date', 'approx', 'approx_note', 'currency']


WaypointFormSetFactory = forms.inlineformset_factory(
    models.Journey,
    models.JourneyWaypoints,
    fields=('waypoint', 'order'),

    can_order=False
)

class JourneyFormSet(forms.ModelForm):
    class Meta:
        model = models.JourneyWaypoints
        fields = ['journey', 'waypoint', 'label']
        js = ('js/jquery.js',)
