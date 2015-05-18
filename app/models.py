from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_countries.fields import CountryField
from forecast.settings import TOKEN_EXPIRATION_PERIOD, ORGANIZATION_TYPE, FORECAST_TYPE

areas = (('1', "Elections"),
         ('2', "Conflicts/Wars"),
         ('3', "Social Events/Protests"),
         ('4', "Fiscal and Monetary Actions"),
         ('5', "Inter-State Negotiations"),
         ('6', "Trade Agreements"),
         ('7', "Private Sector Engagements"))

regions = (('1', "Europe"),
           ('2', "Middle East"),
           ('3', "Africa"),
           ('4', "Asia"),
           ('5', "South Pacific"),
           ('6', "North America"),
           ('7', "South America"))


class Forecast(models.Model):
    forecast_type = models.CharField(max_length=2, choices=FORECAST_TYPE)
    forecast_question = models.TextField(max_length=1000)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()

    def is_active(self):
        this_time = datetime.now()
        if self.end_date <= this_time:
            return True
        return False

    def __unicode__(self):
        return '%s - %s' % (self.id, self.forecast_question)

    class Meta:
        db_table = 'forecasts'
        get_latest_by = 'start_date'
        ordering = ['-end_date']


class Organization(models.Model):

    organization_type = models.CharField(choices=ORGANIZATION_TYPE, max_length=2)
    organization_name = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.organization_type, self.organization_name)


class ForecastVotes(models.Model):
    user_id = models.ForeignKey('UserProfile')
    forecast_id = models.ForeignKey('Forecast')
    vote = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    display_only_username = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey('Organization')
    forecast_areas = models.CommaSeparatedIntegerField(max_length=3, blank=True)
    forecast_regions = models.CommaSeparatedIntegerField(max_length=3, blank=True)

    activation_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(default=False)


class UserForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['activated', 'expires_at', 'activation_token']