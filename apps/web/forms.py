from django import forms
from . import models


class SearchJourney(forms.Form):
    city_from = forms.CharField()
    city_to = forms.CharField()


class Journey(forms.ModelForm):
    #waypoints_count = forms.CharField(widget=forms.HiddenInput())
    #waypoints_count = forms.CharField()

    class Meta:
        model = models.Journey
        fields = ['seats', 'date', 'approx', 'approx_note', 'currency']

    def __init__(self, *args, **kwargs):
        #extra_fields = kwargs.pop('extra', 0)

        #self.fields['waypoints_count'].initial = extra_fields

        super(Journey, self).__init__(*args, **kwargs)

        #for index in range(int(extra_fields)):
        if True:
            index=''
            # generate extra fields in the number specified via extra_fields
            self.fields['waypoint_{index}_place[]'.format(index=index)] = \
                forms.CharField(required=False)
            self.fields['waypoint_{index}_note[]'.format(index=index)] = \
                forms.CharField(required=False)
            self.fields['waypoint_{index}_output_only[]'.format(index=index)] = \
                forms.BooleanField(required=False)
            self.fields['waypoint_{index}_price[]'.format(index=index)] = \
                forms.FloatField(required=False)


class JourneyFormSet(forms.ModelForm):
    class Meta:
        model = models.JourneyWaypoints
        fields = ['journey', 'waypoint', 'label']