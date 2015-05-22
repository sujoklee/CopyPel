import django.forms as forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext, ugettext_lazy as _

from Peleus.settings import ORGANIZATION_TYPE, AREAS, REGIONS, APP_NAME
from forecast.models import CustomUserProfile


class SignupCompleteForm(forms.Form):
    forecast_areas = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=AREAS)
    forecast_regions = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=REGIONS)


class UserRegistrationForm(ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Name')
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Surname')
    display_only_username = forms.BooleanField(widget=forms.CheckboxInput(),
                                               label="Please only display my Username on {}".format(APP_NAME),
                                               required=False)
    agree_with_terms = forms.BooleanField(widget=forms.CheckboxInput(),
                                          label="I agree to {}'s Terms of Use".format(APP_NAME), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}), label='Username')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-sm"}), label="Password")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-sm"}),
                                    label='Confirm Password')
    captcha = ReCaptchaField()
    organization = forms.ChoiceField(widget=forms.RadioSelect(),
                                     choices=ORGANIZATION_TYPE,
                                     label='Organization', required=False)
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm"}),
                                        label='Name of organisation')

    class Meta:
        model = CustomUserProfile
        fields = ("name", "surname", 'display_only_username', "username", "password",
                  "password_conf", "email", "country", "city", "profession", "position", 'organization_name',
                  "organization", "captcha", "agree_with_terms")
        exclude = ['user', 'activation_token', 'expires_at', 'email_verified']
        widgets = {'country': CountrySelectWidget(attrs={'class': "form-control input-sm"}),
                   'name': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'password': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'city': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'profession': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   'position': forms.TextInput(attrs={'class': "form-control input-sm"}),
                   }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password_conf")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        data = self.cleaned_data
        user = User(username=data['username'], first_name=data['name'], last_name=data['surname'], email=data['email'],
                    password=make_password(data['password']))
        user.set_password(data['password'])
        if commit:
            user.save()
        user_profile = CustomUserProfile(user=user, country=data['country'], city=data['city'],
                                         profession=data['profession'], position=data['position'],
                                         organization_name=data['organization_name'],
                                         organization=data['organization'],
                                         display_only_username=data['display_only_username'])
        if commit:
            user_profile.save()
        return user
