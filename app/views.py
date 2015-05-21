import models
import json
import re
import libs.mongo_utils as mongo_utils

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import SignInForm, SignUpForm, ForecastForm, OrganizationForm
from libs.utils import encrypt, createHash
from response_errors import signup_errors
import traceback
from datetime import datetime
from app.models import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from models import CustomUserProfile, UserRegistrationForm
from libs.utils import generate_activation_key
from libs.email_sender import CustomEmailSender
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from forecast.settings import TOKEN_LENGTH, DEFAULT_EMAIL, EMAIL_TEMPLATE_PATH

common_context = {"app_name": settings.APP_NAME}


def authenticated(method):
    def wrapper(*args, **kwargs):
        request = args[1]
        sess_cookie = request.COOKIES.get('sessionid')
        if sess_cookie is not None:
            try:
                Session.objects.get(pk=sess_cookie)
                return method(*args, **kwargs)
            except:
                pass
        return HttpResponseRedirect(reverse('authorize'))

    return wrapper


def mixcontext(session_context=None, *args):
    """
    This function extends common context dictionary with session dictionary
    and any custom dictionary values provided as positional arguments

    :param session_context: session dict which should contain user data
    :param args: any dictionaries
    :return: updated common context
    """
    ret = dict()
    sess_context = {}
    try:
        sess_context['session'] = session_context['user']
    except KeyError:
        sess_context = {}

    ret = dict(sess_context.items() + common_context.items())
    for item in args:
        if isinstance(item, dict) and item:
            ret = dict(ret.items() + item.items())
    return ret


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        request.session.set_test_cookie()

        overall_predictions = mongo_utils.get_overall_predictions()

        for op in overall_predictions:
            forecast_id = int(op['forecast_id'])
            forecast = models.Forecast.objects.get(
                forecast_id=forecast_id
            )

            op['forecast_question'] = forecast.forecast_question

        dict_to_mix = {}
        if len(overall_predictions):
            dict_to_mix.update({'forecasts': overall_predictions})

        context = mixcontext(
            request.session,
            dict_to_mix,
        )
        return render(request, self.template_name, context)


class ActiveForecastsView(View):
    template_name = "active_forecasts.html"

    def get(self, request):
        request.session.set_test_cookie()

        overall_predictions = mongo_utils.get_overall_predictions()

        for op in overall_predictions:
            forecast_id = int(op['forecast_id'])
            forecast = models.Forecast.objects.get(
                forecast_id=forecast_id
            )

            op['forecast_question'] = forecast.forecast_question
        dict_to_mix = {}
        if len(overall_predictions):
            dict_to_mix.update({'forecasts': overall_predictions})

        context = mixcontext(
            request.session,
            dict_to_mix,
        )
        return render(request, self.template_name, context)


class OrganizationView(View):
    template_name = "organization.html"

    def get(self, request):
        request.session.set_test_cookie()

        user = models.User.objects.get(
            usr_id=str(request.session['user']['usr_id'])
        )

        if 'organization' in request.GET:
            organization = request.GET.get('organization')
        else:
            organization = user.organization
        overall_predictions = mongo_utils.get_org_predictions(organization=organization)

        for op in overall_predictions:
            forecast_id = int(op['forecast_id'])
            forecast = models.Forecast.objects.get(
                forecast_id=forecast_id
            )

            op['forecast_question'] = forecast.forecast_question

        dict_to_mix = {'organization': organization}
        if len(overall_predictions):
            dict_to_mix.update({'forecasts': overall_predictions, 'len_forecasts': len(overall_predictions)})

        context = mixcontext(
            request.session,
            dict_to_mix,
        )

        return render(request, self.template_name, context)


class Registered2View(View):
    template_name = ''

    def get(self, request):
        return render(request, self.template_name)


class RegisteredView(View):
    template_name = "thanx.html"

    def get(self, request, token):
        form = SignupCompleteForm()
        context = mixcontext(
            request.session,
            {'form': form, 'token': token}
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = SignupCompleteForm(request.POST)
        if form.is_valid():
            form.save()
            current_user = request.user.customuserprofile
            token = generate_activation_key(TOKEN_LENGTH)
            current_user.activation_token = token
            current_user.conditions_accepted = True
            email_sender = CustomEmailSender(DEFAULT_EMAIL, EMAIL_TEMPLATE_PATH)
            email_sender.send_message([request.user.email], 'Please finish registration', token=token)
            current_user.save()
        return HttpResponseRedirect(reverse('registered2'))


class SignInView(View):
    template_name = "sign_in.html"

    def get(self, request):
        request.session.set_test_cookie()
        form = SignInForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    def post(self, request):
        request.session.set_test_cookie()
        if not request.session.test_cookie_worked():
            return HttpResponse("Please enable cookies and try again.")
        request.session.delete_test_cookie()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:    # and user.is_active:
            if not user.conditions_accepted:
                return HttpResponseRedirect(reverse('registered'))
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('Invalid login or password', status=400)


class SignUpView(View):
    template_name = "sign_up.html"

    def get(self, request):
        """
        Shows signup form for new user
        """
        form = UserRegistrationForm()
        context = mixcontext(
            request.session,
            {'form_main': form,
             }
        )
        return render(request, self.template_name, context)

    def post(self, request):
        """
        This method processes form data and register new user
        """
        signup_form = UserRegistrationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return HttpResponseRedirect(reverse('registered'))

class SignUpAfterView(View):
    template_name = "sign_up_after.html"

class EmailConfirmationView(View):
    template_name = ''  # TODO add template name

    def get(self, request, token):
        res_dict = dict()
        try:
            user = CustomUserProfile.objects.get(activation_token=token)
        except User.DoesNotExist as ex:
            res_dict['error'] = ex
            return render(request, self.template_name, res_dict)
        if token == user.activation_token:
            user.email_verified = True
            res_dict['success'] = 'Email was verified!'
            user.save()
        else:
            res_dict['error'] = 'Provided token is incorrect'
        return render(request, self.template_name, res_dict)


class UserView(View):
    template_name = "user.html"

    def get(self, request, user_id):
        user = models.User.objects.get(usr_id=str(user_id))
        common_context.update(
            user=user
        )
        context = mixcontext(
            request.session,
            {'user': user}
        )
        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = "profile.html"

    def get(self, request):
        if 'user_id' in request.REQUEST:
            is_self = False
            usr_id = request.REQUEST['user_id']
        else:
            is_self = True
            usr_id = str(request.session['user']['usr_id'])

        user = models.User.objects.get(
            usr_id=usr_id
        )

        usr_id = user.usr_id
        all_predictions = mongo_utils.get_predictions_for_user(usr_id=usr_id)
        print all_predictions
        _all_predictions = []
        for prediction in all_predictions:
            forecast_id = prediction['forecast_id']
            forecast = models.Forecast.objects.get(
                forecast_id=forecast_id
            )
            _this_prediction = {'forecast': forecast, 'current_user_prediction': prediction['current_prediction'],
                                'user_time_series': prediction['time_series']}

            existing_peleus_prediction = mongo_utils.get_overall_prediction(forecast_id=forecast_id)
            if existing_peleus_prediction:
                _this_prediction.update({'current_peleus_prediction': existing_peleus_prediction['current_prediction']})
                _this_prediction.update({'peleus_time_series': existing_peleus_prediction['time_series']})

            existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,
                                                                              forecast_id=forecast_id)
            if existing_organization_prediction:
                _this_prediction.update(
                    {'current_org_prediction': existing_organization_prediction['current_prediction']})
                _this_prediction.update({'org_time_series': existing_organization_prediction['time_series']})
            _all_predictions.append(_this_prediction)
        context = mixcontext(
            request.session,
            {'user': user, 'predictions': _all_predictions, 'len_predictions': len(_all_predictions),
             'is_self': is_self},
        )
        return render(request, self.template_name, context)


class ForecastView(View):
    template_name = "forecast.html"

    def get(self, request):
        forecast_id = int(request.GET.get('forecast_id'))
        forecast = models.Forecast.objects.get(
            forecast_id=forecast_id
        )
        usr_id = str(request.session['user']['usr_id'])

        user = models.User.objects.get(
            usr_id=str(request.session['user']['usr_id'])
        )

        dict_to_mix = {
            'user': user,
            'forecast': forecast,
        }

        existing_prediction = mongo_utils.get_prediction(usr_id=usr_id, forecast_id=forecast_id)
        if existing_prediction:
            dict_to_mix.update({'current_prediction': existing_prediction['current_prediction']})
            dict_to_mix.update({'user_time_series': existing_prediction['time_series']})

        existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,
                                                                          forecast_id=forecast_id)
        if existing_organization_prediction:
            dict_to_mix.update({'current_org_prediction': existing_organization_prediction['current_prediction']})
            dict_to_mix.update({'org_time_series': existing_organization_prediction['time_series']})

        context = mixcontext(
            request.session,
            dict_to_mix,
        )
        return render(request, self.template_name, context)

    def post(self, request):
        forecast_id = int(request.POST.get('forecast_id'))
        usr_id = str(request.session['user']['usr_id'])
        user = models.User.objects.get(
            usr_id=str(request.session['user']['usr_id'])
        )
        organization = user.organization
        existing_prediction = mongo_utils.get_prediction(usr_id=usr_id, forecast_id=forecast_id)
        answer = float(request.POST.get('answer'))
        timestamp = unix_time_millis(datetime.now())
        if existing_prediction:
            existing_prediction['time_series'].append({'timestamp': timestamp, 'answer': answer})
            existing_prediction['current_prediction'] = answer
            mongo_utils.save_prediction(existing_prediction)
        else:
            prediction = {'usr_id': usr_id, 'organization': user.organization, 'forecast_id': forecast_id,
                          'current_prediction': answer, 'time_series': [{'timestamp': timestamp, 'answer': answer}]}
            mongo_utils.save_prediction(prediction)

        existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,
                                                                          forecast_id=forecast_id)
        if existing_organization_prediction:
            new_avg = mongo_utils.get_average_org_prediction(organization, forecast_id)
            if new_avg:
                existing_organization_prediction['time_series'].append({'timestamp': timestamp, 'answer': new_avg})
                existing_organization_prediction['current_prediction'] = new_avg
                mongo_utils.save_org_prediction(existing_organization_prediction)
            else:
                print "There was an error in getting org average"
        else:
            prediction = {'organization': user.organization, 'forecast_id': forecast_id, 'current_prediction': answer,
                          'time_series': [{'answer': answer, 'timestamp': timestamp}]}
            mongo_utils.save_org_prediction(prediction)

        existing_overall_prediction = mongo_utils.get_overall_prediction(forecast_id=forecast_id)
        if existing_overall_prediction:
            new_avg = mongo_utils.get_average_prediction(forecast_id)
            if new_avg:
                existing_overall_prediction['time_series'].append({'timestamp': timestamp, 'answer': new_avg})
                existing_overall_prediction['current_prediction'] = new_avg
                mongo_utils.save_overall_prediction(existing_overall_prediction)
            else:
                print "There was an error in getting overall average"
        else:
            prediction = {'forecast_id': forecast_id, 'current_prediction': answer,
                          'time_series': [{'answer': answer, 'timestamp': timestamp}]}
            mongo_utils.save_overall_prediction(prediction)

        # return render(request, self.template_name, request.session)
        response = HttpResponseRedirect(reverse('forecast'))
        response['Location'] += '?forecast_id=' + str(forecast_id)
        return response


class CreateOrganizationView(View):
    template_name = "create_organization.html"

    @authenticated
    def get(self, request):
        form = OrganizationForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    # @authenticated
    def post(self, request):
        organization_form = OrganizationForm(request.POST)

        # prepare default response
        response = {
            'form': 'invalid',
            'errors': []
        }

        cleaned_data = organization_form.data
        organization_name = cleaned_data['organization_name']
        organization_type = cleaned_data['organization_type']

        data = {}
        data['organization_id'] = models.Organization.objects.count() + 1
        data['organization_name'] = organization_name
        data['organization_type'] = organization_type

        organization = models.Organization(**data)
        organization.save()

        response.update({
            'form': 'valid',
        })

        return HttpResponse(
            content=json.dumps(response)
        )


class CreateForecastView(View):
    template_name = "create_forecast.html"

    @authenticated
    def get(self, request):
        form = ForecastForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    @authenticated
    def post(self, request):
        forecast_form = ForecastForm(request.POST)

        # prepare default response
        response = {
            'form': 'invalid',
            'errors': []
        }

        cleaned_data = forecast_form.data
        question = cleaned_data['forecast_question']
        forecast_type = cleaned_data['forecast_type']
        print question
        print forecast_type

        data = {}
        data['forecast_id'] = models.Forecast.objects.count() + 1
        data['forecast_question'] = question
        data['forecast_type'] = forecast_type

        forecast = models.Forecast(**data)
        forecast.save()

        response.update({
            'form': 'valid',
        })

        return HttpResponse(
            content=json.dumps(response)
        )


class LogoutView(View):
    def get(self, request):
        response = logout(request)
        request.session.flush()
        return HttpResponseRedirect(reverse('index'))
