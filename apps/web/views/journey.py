
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, RedirectView, CreateView, UpdateView
from django.views.generic.edit import FormView

from .. import models
from .. import forms
import googlemaps
from pprint import pprint
import pudb
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms as dj_forms


# Create your views here.
# Google API key:  AIzaSyAen5jtHmdJ5ZW3ZOCoqDVjZLkDlILJ014

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, RedirectView, View
from . import models
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from emailusernames.utils import create_user


from django.http import HttpResponse, HttpResponseRedirect

## Import forms
from . import forms


def index(request):
    return render(request, 'web/index.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('../../') ## TODO: OPRAVIT, vyvaruj se absolutnim adresam


class LoginScreen(View):
    header = "Login"

    user_name = None
    user_pass = None
    login_form = forms.LoginForm()
    redirect_bool = False
    info_text = None

    user = None

    def get(self, request):
        return render(request, 'web/login_screen.html', {"form": self.login_form,
                                                         "header": self.header})

    def post(self, request):
        self.user_name = request.POST['user_name']
        self.user_pass = request.POST['user_pass']
        self._check_credentials()

        if self.user:
            login(request, self.user)
            return HttpResponseRedirect('../../')
        else:
            return HttpResponse("INVALID CREDENTIALS!")

    def _check_credentials(self):
        if self.user_name and self.user_pass:
            self.user = authenticate(email=self.user_name,
                                     password=self.user_pass)
        else:
            return HttpResponse("MISSING CREDENTIALS!")


class RegisterScreen(View):
    header = "User Registration"

    user_mail = None
    user_mail_confirm = None
    user_pass = None
    user_pass_confirm = None
    register_form = forms.RegisterForm()

    correct_day = None
    asked_day = None

    question_ok = False
    user_exists = False

    correct_details = {}

    request = None

    def get(self, request):
        return render(request, 'web/register.html', {"form": self.register_form,
                                                     "header": self.header})

    def post(self, request):
        self.correct_day = self.register_form.correct_day
        self.request = request

        self._post_get_details()
        self._check_security_question()
        self._check_details()
        self._check_existing_user()

        if self.user_exists:
            return HttpResponse("ERROR: USER ALREADY EXISTS!")
        else:
            new_user = create_user(email = self.user_mail, password = self.user_pass)
            new_user.save()
            return HttpResponse("SUCCESS: USER CREATED")

        #return render(request, 'web/register.html', {"form": self.register_form})


    def _post_get_details(self):
        self.user_mail = self.request.POST['user_email']
        self.user_mail_confirm = self.request.POST['user_email_confirm']
        self.user_pass = self.request.POST['user_password']
        self.user_pass_confirm = self.request.POST['user_password_confirm']

        self.asked_day = self.request.POST['random_antibot']


    def _check_security_question(self):
        self.correct_day = self.register_form.correct_day
        if self.correct_day == self.asked_day:
            self.question_ok = True
        else:
            return HttpResponse("ERROR: INVALID CONTROL ANSWER!")


    def _check_details(self):
        self.correct_details.update({"correct_name": self.user_mail == self.user_mail_confirm})
        self.correct_details.update({"correct_pass": self.user_pass == self.user_pass_confirm})

        if False in self.correct_details:
            return HttpResponse("ERROR: Some data you entered does not match")


    def _check_existing_user(self):
        test_auth = authenticate(username = self.user_mail,
                                 password = self.user_pass,
                                 email = self.user_mail)
        if test_auth:
            self.user_exists = True
        else:
            self.user_exists = False



class Car(View):
    header = "Car Management page"

    model = None
    owner = None
    name = None
    color = None

    air_conditioning = False
    animals_allowed = False
    has_wifi = False
    has_highway_sign = False
    smoking_allowed = False

    register_sign = None
    reg_notice = ("NOTE", "If you really don't want to, you DO NOT have\
                     to enter your national car sign. Hovever, if\
                    you fill it, you will make it easier for\
                     passengers to find you.")

    form = forms.CarManageForm()
    inp_method = None
    message = None

    def get(self, request):
        self.model = models.Vehicle.objects.filter(owner=request.user)
        return render(request, 'web/cars.html', {"form": self.form,
                                                 "car_list": self.model,
                                                 "message": self.message,
                                                 "reg_notice": self.reg_notice,
                                                 "header": self.header})

    def post(self, request):
        self.inp_method = request.POST.get('method')
        if self.inp_method == 'add_vehicle':
            return self._add_car(request)
        elif self.inp_method == 'remove_vehicle':
            return self._delete_car(request)
        else:
            return HttpResponse("UNKOWN ERROR WITH DATABASE.")

    def _delete_car(self, in_request):
        self.owner = in_request.user
        remove_id = in_request.POST.get('car_id')
        models.Vehicle.objects.filter(owner = self.owner, id = remove_id).delete()
        return HttpResponseRedirect(".")

    def _add_car(self, in_request):
        self.owner = in_request.user
        self.name = in_request.POST.get('car_name')
        self.color = in_request.POST.get('color')

        self.air_conditioning = in_request.POST.get('air_conditioning', False)
        self.animals_allowed = in_request.POST.get('animals_allowed', False)
        self.has_wifi = in_request.POST.get('has_wifi', False)
        self.has_highway_sign = in_request.POST.get('has_highway_sign', False)
        self.smoking_allowed = in_request.POST.get('smoking_allowed', False)

        self.register_sign = in_request.POST.get('register_sign')
        return self._check_required()

    def _check_required(self):
        if self.name and self.color:
            new_car = models.Vehicle(owner=self.owner, name=self.name,
                                     color=self.color, register=self.register_sign,
                                     air_conditioning=self.air_conditioning,
                                     animals_allowed=self.animals_allowed,
                                     wifi_on_board=self.has_wifi,
                                     smoking_allowed=self.smoking_allowed,
                                     highway_mark=self.has_highway_sign)
            new_car.save()
            return HttpResponseRedirect(".")
        else:
            return HttpResponse("FAILED TO SAVE, MISSING DATA!")


class User(View):
    header = "User control panel and information page"
    form = forms.ManageForm

    def get(self, request):
        return render(request, 'web/user.html', {"form": self.form,
                                                 "header": self.header})
    def post(self, request):
        pass

class WaypointNotFound(Exception):
    pass


class JourneyList(ListView, FormView):

    model = models.Journey
    form_class = forms.SearchJourney
    success_url = '/'   # TODO: replace by generic URL of this page
    filter = {
        'city_from': models.Waypoint.objects.filter(pk=3).get(),
        'city_to': models.Waypoint.objects.filter(pk=2).get(),
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
        city_from = self.__city_to_waypoint_model(form.data['city_from'])
        city_to = self.__city_to_waypoint_model(form.data['city_to'])
        self.filter['city_from'] = city_from
        self.filter['city_to'] = city_to
        return super(JourneyList, self).form_valid(form)

    def get_queryset(self):
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
        '''.format(self.filter['city_from'].id, self.filter['city_to'].id)
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


class UserDetail(DetailView):
    model = models.User


# http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/
class JourneyCreate(CreateView):
    template_name = 'web/journey_create2.html'
    model = models.Journey
    form_class = forms.Journey

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form_wpt = forms.WaypointNewFormSetFactory()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form_wpt = forms.WaypointNewFormSetFactory(self.request.POST)
        #print(form.is_valid(), form_wpt.is_valid())
        if form.is_valid() and form_wpt.is_valid():
            return self.form_valid(form, form_wpt)
        else:
            return self.form_invalid(form, form_wpt)

    def form_valid(self, form, form_wpt):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """

        #pprint(form.cleaned_data)
        #print(form_wpt.cleaned_data)
        self.object = form.save()
        form_wpt.instance = self.object
        form_wpt.save()

        return HttpResponseRedirect(
            reverse('journey_detail',
                    kwargs={'pk': self.object.pk}
            )
        )

    def form_invalid(self, form, form_wpt):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt))


class JourneyUpdate(UpdateView):
    template_name = 'web/journey_create2.html'
    model = models.Journey
    form_class = forms.Journey
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """

        super(JourneyUpdate, self).get(request, *args, **kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        qs = models.JourneyWaypoints.objects.filter(
            journey=self.object).order_by('order')

        form_wpt = forms.WaypointUpdateFormSetFactory(
            instance=self.object,
            queryset=qs
        )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                form_wpt=form_wpt,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form_wpt = forms.WaypointUpdateFormSetFactory(self.request.POST,
                                                      instance=self.object)
        #print(form.is_valid(), form_wpt.is_valid())

        if form.is_valid() and form_wpt.is_valid():
            return self.form_valid(form, form_wpt)
        else:
            return self.form_invalid(form, form_wpt)

    def form_valid(self, form, form_wpt):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        #pprint(form.cleaned_data)
        #pprint(form_wpt.cleaned_data)
        form.save()
        form_wpt.save()
        return HttpResponseRedirect(
            reverse('journey_detail',
                    kwargs={'pk': self.object.pk}
            )
        )

    def form_invalid(self, form, form_wpt):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        super(JourneyUpdate, self).form_invalid(form)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  form_wpt=form_wpt))
