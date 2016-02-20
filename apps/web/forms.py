from django import forms
from . import models


class SearchJourney(forms.Form):
    city_from = forms.CharField()
    city_to = forms.CharField()


class Journey(forms.ModelForm):
    own = forms.CharField(help_text='own_help_text', label='own_label')
    #waypoints_count = forms.CharField(widget=forms.HiddenInput())
    waypoints_count = forms.CharField()

    class Meta:
        model = models.Journey
        fields = ['seats', 'date', 'approx', 'approx_note', 'currency']

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(Journey, self).__init__(*args, **kwargs)
        self.fields['waypoints_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['waypoint_{index}_place'.format(index=index)] = \
                forms.CharField()
            self.fields['waypoint_{index}_note'.format(index=index)] = \
                forms.CharField()
            self.fields['waypoint_{index}_output_only'.format(index=index)] = \
                forms.BooleanField()
            self.fields['waypoint_{index}_price'.format(index=index)] = \
                forms.FloatField()
