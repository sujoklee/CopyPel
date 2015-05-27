from datetime import datetime
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models

from Peleus.settings import ORGANIZATION_TYPE, FORECAST_TYPE


class CustomUserProfile(models.Model):
    user = models.OneToOneField(User)
    display_only_username = models.BooleanField(default=False)
    country = CountryField(blank=False)
    city = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    organization = models.CharField(choices=ORGANIZATION_TYPE, max_length=2)
    organization_name = models.TextField(blank=True)
    forecast_areas = models.CommaSeparatedIntegerField(max_length=3, blank=True)
    forecast_regions = models.CommaSeparatedIntegerField(max_length=3, blank=True)

    activation_token = models.TextField(blank=True, max_length=256)
    expires_at = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    conditions_accepted = models.BooleanField(default=False)


class Forecast(models.Model):
    forecast_type = models.CharField(max_length=2, choices=FORECAST_TYPE)
    forecast_question = models.TextField(max_length=1000)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()

    def is_active(self):
        return self.end_date <= datetime.now()

    def __unicode__(self):
        return '%s - %s' % (self.id, self.forecast_question)

    _forecast_types = dict(FORECAST_TYPE)

    def to_json(self):
        return {
            'id': self.id,
            'forecastType': self._forecast_types[self.forecast_type],
            'forecastQuestion': self.forecast_question,
            'startDate': self.start_date.strftime('%Y-%m-%d'),
            'endDate': self.end_date.strftime('%Y-%m-%d'),
            'votes': [{'userId': v.user_id.id, 'vote': v.vote} for v in self.votes.all()]}

    class Meta:
        db_table = 'forecasts'
        get_latest_by = 'start_date'
        ordering = ['-end_date']


class ForecastVotes(models.Model):
    user_id = models.ForeignKey(User)
    forecast_id = models.ForeignKey('Forecast', related_name='votes')
    vote = models.IntegerField()
