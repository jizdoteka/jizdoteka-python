from django.contrib import admin
from django.contrib.auth.models import User
from . import models

# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Waypoint)
admin.site.register(models.Passanger)
admin.site.register(models.Car)
admin.site.register(models.JourneyWaypoints)


class UserProfileInline(admin.TabularInline):
    model = models.UserProfile


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class JourneyWaypointsInline(admin.TabularInline):
    model = models.JourneyWaypoints


# class PassengerOnWaypointInline(admin.TabularInline):
#     model = models.PassengerOnWaypoint


class JourneyAdmin(admin.ModelAdmin):
    inlines = [
        JourneyWaypointsInline,
        # PassengerOnWaypointInline,
    ]

admin.site.register(models.Journey, JourneyAdmin)
