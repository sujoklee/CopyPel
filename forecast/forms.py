import django.forms as forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from captcha.fields import ReCaptchaField
from Peleus.settings import ORGANIZATION_TYPE, AREAS, REGIONS, APP_NAME
from django_countries.widgets import CountrySelectWidget
from forecast.models import CustomUserProfile


class SignupCompleteForm(forms.Form):
    forecast_areas = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=AREAS)
    forecast_regions = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=REGIONS)


class UserRegistrationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Name')
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Surname')
    display_only_username = forms.BooleanField(widget=forms.CheckboxInput(),
                                               label="Please only display my Username on {}".format(APP_NAME),
                                               required=False)
    agree_with_terms = forms.BooleanField(widget=forms.CheckboxInput(),
                                          label="I agree to {}'s Terms of Use".format(APP_NAME), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Username')
    email = forms.EmailField(required=True, label='Email address')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-sm"}), label="Password")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-sm"}),
                                    label='Confirm Password')
    captcha = ReCaptchaField()
    organization = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "form-control input-sm"}),
                                     choices=ORGANIZATION_TYPE,
                                     label='Organization', required=False)
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}),
                                        label='Name of organisation')

    class Meta:
        model = CustomUserProfile
        fields = ("name", "surname", 'display_only_username', "username", "password",
                  "password_conf", "email", "country", "city", "profession", "position", 'organization_name',
                  "organization", "captcha")
        exclude = ['user', 'activation_token', 'expires_at', 'email_verified']
        widgets = {'country': CountrySelectWidget(attrs={'class': "form-control input-sm"}),
                   'name': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'password': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'city': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'profession': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'position': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   }

    def save(self, commit=True):
        data = self.cleaned_data
        user = User(username=data['username'], first_name=data['name'], last_name=data['surname'], email=data['email'],
                    password=data['password'])
        user.save()
        user_profile = CustomUserProfile(user=user, country=data['country'], city=data['city'],
                                         profession=data['profession'], position=data['position'],
                                         organization_name=data['organization_name'],
                                         organization=data['organization'],
                                         display_only_username=data['display_only_username'])
        user_profile.save()
