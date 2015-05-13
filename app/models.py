from django.db import models
from libs.utils import encrypt
from django.forms import ModelForm

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

forecast_type = (('1', 'Binary'),
                 ('2', 'Probability'),
                 ('3', 'Magnitude'),
                 ('4', 'Temporal'))


class Forecast(models.Model):
    forecast_id = models.IntegerField(unique=True)
    forecast_type = models.IntegerField(blank=True)
    forecast_question = models.TextField(blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.name

    class Meta:
        db_table = 'forecasts'


organization_type = (('1', 'School'),
                     ('2', 'Think Tank'),
                     ('3', 'Company'),
                     ('4', 'Government Agency'))


class Organization(models.Model):
    organization_id = models.IntegerField(unique=True)
    organization_type = models.IntegerField(blank=True)
    organization_name = models.TextField(blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.name

    class Meta:
        db_table = 'organizations'


# class ForecastForm(ModelForm):
# class Meta:
#         model = Forecast
#         fields = ['forecast_id', 'forecast_type', 'forecast_question']

class User(models.Model):
    usr_id = models.IntegerField(unique=True)
    display_only_username = models.BooleanField(default=False)
    name = models.TextField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    password = models.TextField()
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    organization = models.TextField(blank=True)
    forecast_areas = models.CommaSeparatedIntegerField(max_length=3, blank=True)
    forecast_regions = models.CommaSeparatedIntegerField(max_length=3, blank=True)
    activation_token = models.TextField(blank=True)

    class Meta:
        db_table = 'users'