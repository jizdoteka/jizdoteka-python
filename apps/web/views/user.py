# -*- coding: utf-8 -*-
import logging
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from .. import forms

logger = logging.getLogger(__name__)


class UserSettingsView(TemplateView):
    template_name = "account/user.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.userform = forms.UserForm(instance=user, prefix='userform')
        self.userprofileform = forms.UserProfileForm(instance=user.userprofile,
                                               prefix='userprofileform')
        return super(UserSettingsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        self.userform = forms.UserForm(
            request.POST,
            instance=user,
            prefix='userform')
        self.userprofileform = forms.UserProfileForm(
            request.POST,
            instance=user.userprofile,
            prefix='userprofileform')

        if self.userform.is_valid() and self.userprofileform.is_valid():
            user = self.userform.save()
            self.userprofileform.save(commit=False)
            self.userprofileform.user = user
            self.userprofileform.save()
            messages.success(request, _('Changes was updated.'))
            return HttpResponseRedirect(reverse_lazy('user-settings'))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UserSettingsView, self).get_context_data(**kwargs)
        context['userform'] = self.userform
        context['userprofileform'] = self.userprofileform
        return context
