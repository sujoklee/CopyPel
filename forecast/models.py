from datetime import date, datetime
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models
from django.db.models import Count, Avg

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
    end_date = models.DateField(blank=True, null=True)

    def is_active(self):
        return self.end_date >= date.today()

    def __unicode__(self):
        return '%s - %s' % (self.id, self.forecast_question)

    def to_json(self):
        return {
            'id': self.id,
            'forecastType': self.get_forecast_type_display(),
            'forecastQuestion': self.forecast_question,
            'startDate': self.start_date.strftime('%Y-%m-%d'),
            'endDate': self.end_date.strftime('%Y-%m-%d'),
            'votes': [{'date': v['date'].strftime('%Y-%m-%d'), 'avgVotes': v['avg_votes']}
                      for v in self.votes.values('date').annotate(avg_votes=Avg('vote'))]}

    def votes_count(self):
        votes = Forecast.objects.filter(pk=self.id).annotate(votes_count=Count('votes')).get().votes_count
        return votes
    votes_count.admin_order_field = 'votes_count'

    class Meta:
        db_table = 'forecasts'
        get_latest_by = 'start_date'
        ordering = ['-end_date']


class ForecastTags(models.Model):
    forecast_id = models.ForeignKey('Forecast')
    tag_id = models.ForeignKey('Tags')


class ForecastPropose(models.Model):
    user_id = models.ForeignKey(User)
    forecast_type_new = models.CharField(max_length=2, choices=FORECAST_TYPE)
    forecast_question_new = models.TextField(max_length=1000)


class ForecastVotes(models.Model):
    user_id = models.ForeignKey(User)
    forecast_id = models.ForeignKey('Forecast', related_name='votes')
    vote = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)

