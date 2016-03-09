"""jizdoteka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.web.views import journey

from apps.web.views.user import UserSettingsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/settings/', UserSettingsView.as_view(), name='user-settings'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', journey.JourneyList.as_view(), name='home'),
    url(r'^new/$', journey.JourneyCreate.as_view(), name='journey_new'),
    url(r'^update/(?P<pk>[0-9]+)$', journey.JourneyUpdate.as_view(), name='journey_update'),
    url(r'^(?P<pk>[0-9]+)$',
        journey.JourneyDetail.as_view(),
        name='journey_detail'
    ),
]
