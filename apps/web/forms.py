from django import forms
from . import models
from random import randint
from . import models
from django.utils.translation import ugettext_lazy as _

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

class RegisterForm(forms.Form):

    def rand_anti_question():
        day_list = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]

        rand_day_num = randint(0, len(day_list))
        rand_addition = randint(0, len(day_list))
        correct_day_num = rand_day_num + rand_addition
        correct_day_index = correct_day_num

        if correct_day_index >= len(day_list):
            correct_day_index = correct_day_index - len(day_list)

        question = "Dnes je %s. V případě, že je toto tvrzení pravdivé, co bude za %s dny?" % (day_list[rand_day_num - 1], rand_addition)
        return (question, day_list[correct_day_index - 1])

    user_email = forms.CharField(max_length = 100, label = _("Your E-Mail address"))
    user_email_confirm = forms.CharField(max_length = 100, label = _("Your E-Mail address - Confirmation"))
    user_password = forms.CharField(widget = forms.PasswordInput(), label = _("Your Password"))
    user_password_confirm = forms.CharField(widget = forms.PasswordInput(), label = _("Your Password - Confirmation"))

    cont_question, correct_day = rand_anti_question()
    random_antibot = forms.CharField(max_length = 50, label = cont_question)


class LoginForm(forms.Form):
    user_name = forms.EmailField(max_length = 100, label = _("Your email"))
    user_pass = forms.CharField(widget = forms.PasswordInput(), label = _("Your Password"))


class ManageForm(forms.Form):
    user_mail = forms.EmailField(max_length = 100, label = _("Your E-mail address"))
    user_mail_confirm = forms.EmailField(max_length = 100, label = _("Your E-mail address - Confirmation"))
    user_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput(), label = _("Your Password"))
    user_pass_confirm = forms.EmailField(max_length = 100, widget = forms.PasswordInput(), label = _("Your Password - Confirmation"))
    user_phone = forms.CharField(max_length = 20, label = _("Your phone number"))


class CarManageForm(forms.Form):
    car_name = forms.CharField(max_length = 20, label = _("Your car brand"))
    #color = forms.CharField(max_length = 10, label = _("Your car's color"))

    air_conditioning = forms.BooleanField(label = _("Air conditioning in car"))
    animals_allowed = forms.BooleanField(label = _("Animal transport is allowed"))
    has_wifi = forms.BooleanField(label = _("Wifi is in car"))
    has_highway_sign = forms.BooleanField(label = _("Car has a Highway stamp"))
    smoking_allowed = forms.BooleanField(label = "Smoking allowed in vehicle")

    register_sign = forms.CharField(max_length = 16, label = _("Car national register sign"))


class CreateJourneyForm(forms.Form):

    pass
