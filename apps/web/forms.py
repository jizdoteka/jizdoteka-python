from django import forms
from . import models
from random import randint

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

    user_email = forms.CharField(max_length = 100, label = "Vaše emailová adresa")
    user_email_confirm = forms.CharField(max_length = 100, label = "Vaše emailová adresa - kontrola")
    user_password = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo")
    user_password_confirm = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo - kontrola")

    cont_question, correct_day = rand_anti_question()
    random_antibot = forms.CharField(max_length = 50, label = cont_question)


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length = 100, label = "Váš email")
    user_pass = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo")


class ManageForm(forms.Form):
    user_mail = forms.EmailField(max_length = 100, label = "Váš email")
    user_mail_confirm = forms.EmailField(max_length = 100, label = "Váš email - kontrola")
    user_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput(), label = "Vaše heslo")
    user_pass_confirm = forms.EmailField(max_length = 100, widget = forms.PasswordInput(), label = "Vaše heslo - kontrola")
    user_phone = forms.CharField(max_length = 20, label = "Vaše telefonní číslo")


class CarManageForm(forms.Form):
    car_name = forms.CharField(max_length = 20, label = "Značka Vašeho vozidla")
    car_color = forms.CharField(max_length = 10, label = "Barva Vašeho vozidla")

    car_air_conditioning = forms.BooleanField(label = "Vozidlo je vybaveno klimatizací")
    car_animals_allowed = forms.BooleanField(label = "Ve vozidle lze převážet zvířata")
    car_has_wifi = forms.BooleanField(label = "Ve vozidle je síť Wi-Fi")
    car_has_highway_sign = forms.BooleanField(label = "Vozidlo má dálniční známku")
    car_smoking_allowed = forms.BooleanField(label = "Ve vozidle se smí kouřit")

    car_register_sign = forms.CharField(max_length = 16, label = "SPZ Vašeho vozidla")
