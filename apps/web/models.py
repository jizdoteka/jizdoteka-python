from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.db import models
from django.conf import settings
from django.db.models import signals
<<<<<<< HEAD
=======

from django.contrib.auth.hashers import check_password
#from django.contrib.gis.db import models as gis_models
>>>>>>> Commit pred rebasem
from django.contrib.auth.models import User


class Vehicle(models.Model):
    name = models.CharField(max_length=20, blank=False)
    owner = models.ForeignKey(User)
    register = models.CharField(max_length=20, blank = True, default = None)
    color = models.CharField(max_length=10, blank=False)

    wifi_on_board = models.BooleanField(default=False)
    animals_allowed = models.BooleanField(default=False)
    highway_mark = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)

    def __str__(self):
        ret_str = "Vehicle basic attrs:\n\
                name: %s, register: %s, \
                color: %s\, owner_id: %s, \
                wifi_on_board: %s, animals_allowed: %s, \
                highway_mark: %s\nsmoking_allowed: %s, \
                air_conditioning: %s" % (self.name, self.register,
                                         self.color, self.owner.id,
                                         self.wifi_on_board, self.animals_allowed,
                                         self.highway_mark,self.smoking_allowed,
                                         self.air_conditioning)
        return ret_str


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=13, blank=True)
    reputation = models.IntegerField(blank=True, default=0)
    mojeid = models.CharField(max_length=100, blank=True)
    num_journeys = models.IntegerField(blank=True, default=0)
    driven_km = models.IntegerField(blank=True, default=0)
    drive_years = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.user.email


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

signals.post_save.connect(create_user_profile, User)


# Create your models here.
class Waypoint(models.Model):
    city = models.CharField(max_length=100)
    #distinct = models.CharField(max_length=100,
    #                            help_text=_('Okres'),
    #                            blank=True,
    #                            null=True)
    lat = models.FloatField(verbose_name=_('Lattitude'), default=0)
    long = models.FloatField(verbose_name=_('Longtitude'), default=0)

    def __str__(self):
        return self.city


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_author'
    )
    recipient = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_recipient'
    )
    date = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return '%s: %s' % (self.author, self.message[:50])


class Journey(models.Model):
    CZK = 'CZK'
    EUR = 'EUR'

    currency_list = (
        (CZK, 'Kc'),
        (EUR, 'Eur'),
    )

    seats = models.IntegerField(
        default=0,
        verbose_name=_('Amount of available seats for this journey')
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date/time of start of journey')
    )
    approx = models.BooleanField(
        default='',
        verbose_name=_('Driver is not sure about exact time of departure')
    )
    approx_note = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('If approx is applied, this can be used for short note '
                       'to departure'))
    waypoints = models.ManyToManyField(Waypoint, through='JourneyWaypoints')
    currency = models.CharField(
        max_length=3,
        choices=currency_list,
        default=CZK,
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        label = self.journeywaypoints_set.order_by('order')
        #return "%s" % self.date
        return '%s -> %s [%s]' % (
            label.first().waypoint.city,
            label.last().waypoint.city,
            self.date
        )


class JourneyWaypoints(models.Model):
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE
    )
    waypoint = models.ForeignKey(
        Waypoint,
        on_delete=models.CASCADE
    )
    label = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text=_('Note about the place, i.e. corner of cross.'),
    )
    # TODO: figure out better name for 'output_only'
    output_only = models.BooleanField(
        default=False,
        blank=True,
        help_text=_('Waypoting is for leaving only.'),
    )
    order = models.IntegerField(
        verbose_name=_('Order number from start'),
        default=0
    )
    segment_price = models.FloatField(
        null=True,
        default=None,
        blank=True,
        verbose_name=_('Partial price of journey'),
        help_text=_(('Price between previous and this waypoint '
                     '(currency is same as set in journey).'))
    )
    # FIXME: restrict creation relation only
    # FIXME: if JourneyWaypoints.journey == Passanger.journey
    passangers = models.ManyToManyField(
        'Passanger',
        blank=True,
    )

    #class Meta:
    #    unique_together = (('journey', 'order'),)

    def __str__(self):
        return '%s [#%s]: %s' % (self.journey, self.order, self.waypoint)

    def free_seats(self):
        return self.journey.seats - self.occupied_seats()

    def occupied_seats(self):
        return self.passangers.filter(state__exact=Passanger.SUBSCRIBED).count()


class Passanger(models.Model):
    SUBSCRIBED = 'subscr'
    UNSUBSCRIBED = 'unsubs'
    REJECTED = 'reject'

    states = (
        (SUBSCRIBED, _('Assigned')),
        (UNSUBSCRIBED, _('Unsubscribed')),
        (REJECTED, _('Rejected by driver')),
    )

    user = models.ForeignKey(User)
    journey = models.ForeignKey(Journey)
    state = models.CharField(
        max_length=6,
        choices=states,
        default=SUBSCRIBED
    )

    def __str__(self):
        return str(self.user) + ' (' + str(self.journey) + ')'
