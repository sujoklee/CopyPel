from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_countries.fields import CountryField
from forecast.settings import TOKEN_EXPIRATION_PERIOD, ORGANIZATION_TYPE, FORECAST_TYPE
from captcha.fields import ReCaptchaField
from django import forms
from django.core import validators
from forecast.settings import APP_NAME
from django_countries.widgets import CountrySelectWidget
from collections import OrderedDict

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

    class Meta:
        db_table = 'organization'


class ForecastVotes(models.Model):
    user_id = models.ForeignKey(User)
    forecast_id = models.ForeignKey('Forecast')
    vote = models.IntegerField()


class CustomUserProfile(models.Model):
    user = models.OneToOneField(User)
    display_only_username = models.BooleanField(default=False)
    country = CountryField(blank=False)
    city = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey('Organization', blank=True)
    forecast_areas = models.CommaSeparatedIntegerField(max_length=3, blank=True)
    forecast_regions = models.CommaSeparatedIntegerField(max_length=3, blank=True)

    activation_token = models.TextField(blank=True, max_length=256)
    expires_at = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(default=False)
    conditions_accepted = models.BooleanField(default=False)

    
class UserRegistrationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label='Name')
    surname = forms.CharField(widget=forms.TextInput(), label='Surname')
    display_only_username = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Please only display my Username on {}".format(APP_NAME),
        required=False)
    agree_with_terms = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="I agree to {}'s Terms of Use".format(APP_NAME),
        required=True)
    username = forms.CharField(
        widget=forms.TextInput(),
        label='Username'
    )

    email = forms.EmailField(required=True, validators=[validators.EmailValidator], label='Email address')
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_conf = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
    organization = forms.ChoiceField(widget=forms.RadioSelect, choices=ORGANIZATION_TYPE,
                                     label='Organization', required=False)

    class Meta:
        model = CustomUserProfile
        fields = ("name", "surname", "username", "password", 
                  "password_conf", "email", "country", "city", "profession", "position", "organization", "captcha")
        exclude = ['user', 'activation_token', 'expires_at', 'email_verified']
        widgets = {'country': CountrySelectWidget(attrs={'class': "form-control"})}

    def save(self, commit=True):
        data = self.cleaned_data
        user = User(username=data['username'], first_name=data['name'], last_name=data['surname'], email=data['email'],
                    password=data['password'])
        user.save()
        user_profile = CustomUserProfile(user=user, country=data['country'], )
        user_profile.save()


class OrganizationForm(ModelForm):
    NAME_MAX = 1000
    NAME_MIN = 1
    organization_name = forms.CharField(
        max_length=NAME_MAX,
        min_length=NAME_MIN,
        widget=forms.TextInput(attrs={'size': NAME_MAX}),
        label='Organization Name',
        required=True)

    organization_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ORGANIZATION_TYPE, required=False)

    class Meta:
        model = Organization
        fields = '__all__'


class SignupCompleteForm(ModelForm):
    forecast_areas = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=areas)
    forecast_regions = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=regions)