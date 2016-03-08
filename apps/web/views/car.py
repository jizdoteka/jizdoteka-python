from django.views.generic import DetailView
from django.shortcuts import render

from .. import forms
from .. import models


class Car(DetailView):
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
