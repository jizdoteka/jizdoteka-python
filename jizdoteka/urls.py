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
from apps.web.views import journey, car

from apps.web.views.user import UserSettingsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/settings/', UserSettingsView.as_view(), name='user-settings'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', journey.JourneyList.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)$',
        journey.JourneyDetail.as_view(),
        name='journey_detail'
    ),
    url(r'^new/$',
        journey.JourneyCreate.as_view(),
        name='journey_new'),
    url(r'^update/(?P<pk>[0-9]+)$',
        journey.JourneyUpdate.as_view(),
        name='journey_update'
    ),
    url(r'^delete/(?P<pk>[0-9]+)$',
        journey.JourneyDelete.as_view(),
        name='journey_delete'
    ),
    url(r'^car/', car.CarList.as_view(),
        name='car_list'
    ),
    url(r'^car/(?P<pk>[0-9]+)', car.CarDetail.as_view(),
        name='car_detail'
    ),
    url(r'^car/delete/(?P<pk>[0-9]+)', car.CarDelete.as_view(),
        name='car_delete'
    ),
    url(r'^car/new', car.CarNew.as_view(),
        name='car_new'
    ),
    url(r'^car/update/(?P<pk>[0-9]+)', car.CarUpdate.as_view(),
        name='car_update'
    ),
]
