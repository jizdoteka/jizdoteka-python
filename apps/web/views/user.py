# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy


class UserSettingsView(UpdateView):
    template_name = "web/user.html"
    model = User
    #form_class = UserSettingsForm
    fields = ["username", "first_name", "last_name"]
    success_url = reverse_lazy("user-settings")

    #def form_valid(self, form):
    #    instance = form.save(commit=False)
    #    if 'icon' in form.files:
    #        try:
    #            userdata = instance.userdata
    #            userdata.icon = form.files['icon']
    #            userdata.save()
    #        except UserData.DoesNotExist:
    #            userdata = UserData(user=instance, icon=form.files['icon'])
    #            userdata.save()
    #            instance.userdata = userdata
    #    messages.success(self.request, _("Settings successfully updated."))
    #    return super(UserSettingsView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user
