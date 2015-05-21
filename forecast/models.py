from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models

from Peleus.settings import ORGANIZATION_TYPE


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
    expires_at = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(default=False)
    conditions_accepted = models.BooleanField(default=False)
