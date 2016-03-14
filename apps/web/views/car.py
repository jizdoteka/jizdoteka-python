from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django import http
from django.contrib import messages

from .. import forms
from .. import models


class CarNew(CreateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'web/car_new.html'
    success_url = reverse_lazy('car_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CarNew, self).form_valid(form)


class CarUpdate(UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'web/car_new.html'
    success_url = reverse_lazy('cars')

    def dispatch(self, request, *args, **kwargs):
        obj = models.Car.objects.filter(pk=kwargs['pk']).filter(
            owner=self.request.user)
        if not obj:
            messages.error(request, _('This car is not yours.'))
            return http.HttpResponseRedirect(reverse_lazy('car_list'))
        return super(CarUpdate, self).dispatch(request, *args, **kwargs)


class CarList(ListView):
    model = models.Car

    def get_queryset(self):
        return models.Car.objects.filter(owner=self.request.user).all()


class CarDetail(DetailView):
    model = models.Car


class CarDelete(DeleteView):
    model = models.Car
