from django import forms
from django.conf import settings
from models import areas, regions, ORGANIZATION_TYPE, FORECAST_TYPE, Organization
from django.core.validators import RegexValidator
import libs.widgets as widgets
import re


class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        super(CustomForm, self).__init__(*args, **kwargs)

    def serialize(self, **kwargs):
        res = {}
        for field in self:
            if not re.match(r'password', field.name):
                res[field.name] = field.value()
        res.update(**kwargs)
        return res

    @property
    def error_list(self):
        for field in self:
            if field.errors:
                err = str(field.errors.as_text())
                res = re.match(r'\*(.+)', err).group(1)
                self.custom_errors.append("{}{}".format(field.label, res))
        return self.custom_errors


class SignInForm(CustomForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        ),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        ),
        label=''
    )


class OrganizationForm(CustomForm):
    NAME_MAX = 1000
    NAME_MIN = 1

    organization_name = forms.CharField(
        max_length=NAME_MAX,
        min_length=NAME_MIN,
        widget=forms.TextInput(
            attrs={
                'ng-model': 'form.data.organization_name',
                'autocomplete': 'off'
            }
        ),
        label='Organization Name',
        required=True)

    organization_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ORGANIZATION_TYPE)

    def clean(self):
        cleaned_data = super(OrganizationForm, self).clean()
        return cleaned_data


class ForecastForm(CustomForm):
    QUESTION_MAX = 1000
    QUESTION_MIN = 1

    forecast_question = forms.CharField(
        max_length=QUESTION_MAX,
        min_length=QUESTION_MIN,
        widget=forms.TextInput(
            attrs={
                'ng-model': 'form.data.question',
                'autocomplete': 'off'
            }
        ),
        label='Question',
        required=True)

    forecast_type = forms.ChoiceField(widget=forms.RadioSelect, choices=FORECAST_TYPE)

    def clean(self):
        cleaned_data = super(ForecastForm, self).clean()
        return cleaned_data


class SignUpForm(CustomForm):
    NAME_MIN = 2
    NAME_MAX = 35
    NAME_REGEX = '^[a-zA-Z\s]+$'
    USRNM_MIN = 3
    USRNM_MAX = 30
    USRNM_REGEX = '^[a-zA-Z][a-zA-Z0-9\_]+$'
    PASSWD_MIN = 6
    PASSWD_MAX = 20
    PASSWD_REGEX = '^[a-zA-Z0-9\_]+$'
    EMAIL_MIN = 6
    EMAIL_MAX = 35
    EMAIL_REGEX = '^[a-z][a-z0-9\_\.\-]+@[a-z0-9\-\_]+\.[a-z]{2,4}$'

    agree_with_terms = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'ng-model': 'form.data.agree_with_terms',
                'ng-true-value': 1,
                'ng-false-value': 0
            }
        ),
        label="I agree to {}'s Terms of Use".format(
            settings.APP_NAME
        ),
        required=False
    )
    display_only_username = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'ng-model': 'form.data.display_only_username',
                'ng-true-value': 1,
                'ng-false-value': 0
            }
        ),
        label="Please only display my Username on {}".format(
            settings.APP_NAME
        ),
        required=False
    )
    name = forms.CharField(
        max_length=NAME_MAX,
        min_length=NAME_MIN,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name',
                'ng-model': 'form.data.name',
                'ng-minlength': 2,
                'ng-pattern': "/{}/".format(NAME_REGEX),
                'required': 'required',
                'autocomplete': 'off'
            }
        ),
        validators=[
            RegexValidator(
                regex=NAME_REGEX,
                message=' is invalid',
                code='invalid_name'
            )
        ],
        label='Name'
    )

    username = forms.CharField(
        max_length=USRNM_MAX,
        min_length=USRNM_MIN,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'ng-model': 'form.data.username',
                'ng-minlength': USRNM_MIN,
                'ng-pattern': "/{}/".format(USRNM_REGEX),
                'required': 'required',
                'autocomplete': 'off'
            }
        ),
        validators=[
            RegexValidator(
                regex=USRNM_REGEX,
                message=' is invalid',
                code='invalid_username'
            ),
        ],
        label='Username'
    )
    password = forms.CharField(
        min_length=PASSWD_MIN,
        max_length=PASSWD_MAX,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'ng-model': 'form.data.password',
                'ng-minlength': PASSWD_MIN,
                'ng-pattern': "/{}/".format(PASSWD_REGEX),
                'required': 'required'
            }
        ),
        validators=[
            RegexValidator(
                regex=PASSWD_REGEX,
                message=' is invalid',
                code='invalid_password'
            ),
        ],
        label='Password'
    )
    password_conf = forms.CharField(
        min_length=PASSWD_MIN,
        max_length=PASSWD_MAX,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'ng-model': 'form.data.password_conf',
                'ng-minlength': PASSWD_MIN,
                'ng-pattern': "/{}/".format(PASSWD_REGEX),
                'required': 'required'
            }
        ),
        validators=[
            RegexValidator(
                regex=PASSWD_REGEX,
                message=' is invalid',
                code='invalid_password_conf'
            ),
        ],
        label='Confirm Password'
    )
    email = forms.EmailField(
        max_length=EMAIL_MAX,
        min_length=EMAIL_MIN,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'ng-model': 'form.data.email',
                   'ng-pattern': "/{}/".format(EMAIL_REGEX),
                   'type': 'email',
                   'required': 'required',
                   'autocomplete': 'off'}
        ),
        validators=[
            RegexValidator(
                regex=EMAIL_REGEX,
                message=' is invalid',
                code='invalid_email'
            )
        ],
        label='Email'
    )
    country = forms.CharField(
        max_length=30,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Country',
                'ng-model': 'form.data.country',
                'ng-pattern': "/{}/".format(NAME_REGEX),
                'required': 'required'
            }
        ),
        validators=[
            RegexValidator(
                regex=NAME_REGEX,
                message=' is invalid',
                code='invalid_country'
            ),
        ],
        label='Country'
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City',
                'ng-model': 'form.data.city',
                'ng-pattern': "/{}/".format(NAME_REGEX)
            }
        ),
        validators=[
            RegexValidator(
                regex=NAME_REGEX,
                message=' is invalid',
                code='invalid_city'
            ),
        ],
        label='City',
        required=False
    )
    profession = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Profession',
                'ng-model': 'form.data.profession',
                'ng-pattern': "/{}/".format(NAME_REGEX)
            }
        ),
        validators=[
            RegexValidator(
                regex=NAME_REGEX,
                message=' is invalid',
                code='invalid_profession'
            ),
        ],
        label='Profession',
        required=False
    )
    choices = []
    for org in Organization.objects.all():
        choices.append((org.id, org.organization_name))
    # print choices
    # organization = forms.CharField(
    # widget=forms.TextInput(
    #         attrs={
    #             'placeholder': 'Organization/Employer',
    #             'ng-model': 'form.data.organization',
    #             'ng-pattern': "/{}/".format(NAME_REGEX)
    #         }
    #     ),
    #     validators=[
    #         RegexValidator(
    #             regex=NAME_REGEX,
    #             message=' is invalid',
    #             code='invalid_organization'
    #         ),
    #     ],
    #     label='Organization',
    #     required=False
    # )

    organization = forms.ChoiceField(widget=forms.RadioSelect, choices=choices, label='Organization', required=False)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        try:
            pass1 = cleaned_data['password']
            pass2 = cleaned_data['password_conf']
            if pass1 != pass2:
                raise forms.ValidationError('Passwords do not match')
            cleaned_data.pop('password_conf')
        except KeyError:
            pass
        return cleaned_data


class SignupCompleteForm(CustomForm):
    forecast_areas = forms.MultipleChoiceField(
        choices=areas,
        widget=widgets.CheckboxSelectMultiple(
            attrs={
                'checklist-model': 'form.data.forecast_areas'
            }
        ),
        required=False
    )
    forecast_regions = forms.MultipleChoiceField(
        choices=regions,
        widget=widgets.CheckboxSelectMultiple(
            attrs={
                'checklist-model': 'form.data.forecast_regions'
            }
        ),
        required=False
    )