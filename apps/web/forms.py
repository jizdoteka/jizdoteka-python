from django import forms
from . import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SearchJourney(forms.Form):
    city_from = forms.CharField()
    city_to = forms.CharField()


class Journey(forms.ModelForm):
    #def __init__(self, user, *args, **kwargs):
    #    super(Journey, self).__init__(*args, **kwargs)
    #    car = models.Car.objects.filter(owner=user)
    #    self.fields['car'].queryset = car

    #car = forms.ModelChoiceField(
    #    queryset=None,
    #    empty_label=None,
    #    to_field_name='name',
    #    label='Car'
    #)

    class Meta:
        model = models.Journey
        fields = ['seats', 'car', 'date', 'approx', 'approx_note', 'currency']


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


class CarForm(forms.ModelForm):
    class Meta():
        model = models.Car
        fields = '__all__'
        exclude = ('owner',)


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)
