import models
import json
import re
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from .forms import SignInForm, SignUpForm, SignupCompleteForm, ForecastForm, OrganizationForm
from libs.utils import encrypt, createHash
from response_errors import signup_errors
import traceback
from datetime import datetime
import libs.mongo_utils as mongo_utils

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
    except:
        sess_context = {}
    print(common_context, sess_context)
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
            dict_to_mix.update({'forecasts':overall_predictions})

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
            dict_to_mix.update({'forecasts':overall_predictions})

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

        dict_to_mix = {'organization':organization}
        if len(overall_predictions):
            dict_to_mix.update({'forecasts':overall_predictions,'len_forecasts':len(overall_predictions)})

        context = mixcontext(
            request.session,
            dict_to_mix,
        )

        return render(request, self.template_name, context)

class RegisteredView(View):
    template_name = "thanx.html"

    def get(self, request, token):
        form = SignupCompleteForm()
        context = mixcontext(
            request.session,
            {'form': form, 'token': token}
        )
        return render(request, self.template_name, context)

    def post(self, request, token):
        post_data = dict(request.POST)
        # Need to remove both keys 'cause angular sets them in controller
        post_data.pop('agree_with_terms')
        post_data.pop('display_only_username')

        areas = request.POST.getlist('forecast_areas[]')
        regions = request.POST.getlist('forecast_regions[]')

        form = SignupCompleteForm(post_data)
        response = {
            'form': 'invalid',
            'form_data': form.serialize(
                forecast_areas=areas,
                forecast_regions=regions
            ),
            'errors': []
        }

        if form.is_valid():
            try:
                user = models.User.objects.get(activation_token=token)
            except models.User.DoesNotExist:
                user = []
                response['errors'].append(
                    signup_errors['profile_update_prohibited']
                )
            if user:
                try:
                    user.forecast_areas = areas
                    user.forecast_regions = regions
                    user.activation_token = ''
                    user.save()
                    response.update(
                        form='valid',
                        location=reverse('index')
                    )
                    response.pop('form_data')

                    # log new user in
                    request.session['user'] = {
                        'usr_id': user.usr_id,
                        'email': user.email,
                        'username': user.username
                    }
                    return HttpResponse(content=json.dumps(response))
                except:
                    response['errors'].append(
                        signup_errors['profile_update_failed']
                    )
        print(response)

        return HttpResponse(content=json.dumps(response))


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
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            for sesskey in request.session.keys():
                del request.session[sesskey]
            try:
                user = models.User.objects.get(
                    username=request.POST['username'],
                    password=encrypt(encrypt(request.POST['password']))
                )
                if user:
                    request.session['user'] = {
                        'usr_id': user.usr_id,
                        'email': user.email,
                        'username': user.username
                    }
                    return HttpResponseRedirect('/')
            except models.User.DoesNotExist:
                pass
            return HttpResponseRedirect(reverse('authorize'))
        else:
            return HttpResponse("Please enable cookies and try again.")


class SignUpView(View):
    template_name = "sign_up.html"

    def get(self, request):
        """
        Shows signup form for new user
        """
        form = SignUpForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    def post(self, request):
        """
        This method processes form data and register new user
        """
        signup_form = SignUpForm(request.POST)

        # prepare default response
        response = {
            'form': 'invalid',
            'form_data': signup_form.serialize(
                display_only_username=request.POST.get('display_only_username')
            ),
            'errors': []
        }

        agree = request.POST.get('agree_with_terms')
        display_only_username = request.POST.get('display_only_username')

        if signup_form.is_valid():
            # log previous user out before register
            try:
                del request.session['user']
            except KeyError:
                pass
            data = signup_form.cleaned_data
            try:
                existing_user = models.User.objects.filter(
                    Q(username=data['username']) | Q(email=data['email'])
                )
            except models.User.DoesNotExist:
                existing_user = []
            if existing_user:
                response['errors'].append(
                    signup_errors['profile_exists']
                )
            else:
                if agree == u'1':
                    data.pop('agree_with_terms')
                    try:
                        data['display_only_username'] = True \
                            if display_only_username == u'1' else False
                        data['usr_id'] = models.User.objects.count() + 1
                        data['activation_token'] = createHash()
                        data['password'] = encrypt(encrypt(data['password']))
                        user = models.User(**data)
                        user.save()
                        response.update({
                            'form': 'valid',
                            'location': reverse(
                                'registered',
                                kwargs={'token': data['activation_token']}
                            )
                        })
                        response.pop('form_data')
                    except:
                        response['errors'].append(
                            signup_errors['profile_create_failed']
                        )
                else:
                    response['errors'].append(
                        signup_errors['profile_confirm_terms']
                    )

        response['errors'] += signup_form.error_list \
            + signup_form.non_field_errors()
        return HttpResponse(
            content=json.dumps(response)
        )


class UserView(View):
    template_name = "user.html"

    @authenticated
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

    # @authenticated
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
            _this_prediction = {'forecast':forecast,'current_user_prediction':prediction['current_prediction'],'user_time_series':prediction['time_series']}

            existing_peleus_prediction = mongo_utils.get_overall_prediction(forecast_id=forecast_id)
            if existing_peleus_prediction:
                _this_prediction.update({'current_peleus_prediction':existing_peleus_prediction['current_prediction']})
                _this_prediction.update({'peleus_time_series':existing_peleus_prediction['time_series']})

            existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,forecast_id=forecast_id)
            if existing_organization_prediction:
                _this_prediction.update({'current_org_prediction':existing_organization_prediction['current_prediction']})
                _this_prediction.update({'org_time_series':existing_organization_prediction['time_series']})
            _all_predictions.append(_this_prediction)
        context = mixcontext(
            request.session,
            {'user': user,'predictions':_all_predictions,'len_predictions':len(_all_predictions),'is_self':is_self},
        )
        return render(request, self.template_name, context)

class ForecastView(View):
    template_name = "forecast.html"

    # @authenticated
    def get(self, request):
        forecast_id = int(request.GET.get('forecast_id'))
        forecast = models.Forecast.objects.get(
            forecast_id=forecast_id
        )
        usr_id=str(request.session['user']['usr_id'])

        user = models.User.objects.get(
            usr_id=str(request.session['user']['usr_id'])
        )

        dict_to_mix = {
            'user':user,
            'forecast':forecast,
        }

        existing_prediction = mongo_utils.get_prediction(usr_id=usr_id,forecast_id=forecast_id)
        if existing_prediction:
            dict_to_mix.update({'current_prediction':existing_prediction['current_prediction']})
            dict_to_mix.update({'user_time_series':existing_prediction['time_series']})

        existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,forecast_id=forecast_id)
        if existing_organization_prediction:
            dict_to_mix.update({'current_org_prediction':existing_organization_prediction['current_prediction']})
            dict_to_mix.update({'org_time_series':existing_organization_prediction['time_series']})

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
        existing_prediction = mongo_utils.get_prediction(usr_id=usr_id,forecast_id=forecast_id)
        answer = float(request.POST.get('answer'))
        timestamp = unix_time_millis(datetime.now())
        if existing_prediction:
            existing_prediction['time_series'].append({'timestamp':timestamp,'answer':answer})
            existing_prediction['current_prediction'] = answer
            mongo_utils.save_prediction(existing_prediction)
        else:
            prediction = {'usr_id':usr_id,'organization':user.organization,'forecast_id':forecast_id,'current_prediction':answer,'time_series':[{'timestamp':timestamp,'answer':answer}]}
            mongo_utils.save_prediction(prediction)

        existing_organization_prediction = mongo_utils.get_org_prediction(organization=user.organization,forecast_id=forecast_id)
        if existing_organization_prediction:
            new_avg = mongo_utils.get_average_org_prediction(organization,forecast_id)
            if new_avg:
                existing_organization_prediction['time_series'].append({'timestamp':timestamp,'answer':new_avg})
                existing_organization_prediction['current_prediction'] = new_avg
                mongo_utils.save_org_prediction(existing_organization_prediction)
            else:
                print "There was an error in getting org average"
        else:
            prediction = {'organization':user.organization,'forecast_id':forecast_id,'current_prediction':answer,'time_series':[{'answer':answer,'timestamp':timestamp}]}
            mongo_utils.save_org_prediction(prediction)
        
        existing_overall_prediction = mongo_utils.get_overall_prediction(forecast_id=forecast_id)
        if existing_overall_prediction:
            new_avg = mongo_utils.get_average_prediction(forecast_id)
            if new_avg:
                existing_overall_prediction['time_series'].append({'timestamp':timestamp,'answer':new_avg})
                existing_overall_prediction['current_prediction'] = new_avg
                mongo_utils.save_overall_prediction(existing_overall_prediction)
            else:
                print "There was an error in getting overall average"
        else:
            prediction = {'forecast_id':forecast_id,'current_prediction':answer,'time_series':[{'answer':answer,'timestamp':timestamp}]}
            mongo_utils.save_overall_prediction(prediction)

        # return render(request, self.template_name, request.session)
        response = HttpResponseRedirect(reverse('forecast'))
        response['Location'] += '?forecast_id='+str(forecast_id)
        return response

class CreateOrganizationView(View):
    template_name = "create_organization.html"

    @authenticated
    def get(self,request):
        form = OrganizationForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    # @authenticated
    def post(self,request):
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
    def get(self,request):
        form = ForecastForm()
        context = mixcontext(
            request.session,
            {'form': form}
        )
        return render(request, self.template_name, context)

    @authenticated
    def post(self,request):
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
        for sesskey in request.session.keys():
            del request.session[sesskey]
        request.session.flush()
        from django.contrib.auth.views import logout
        response = logout(request, 'index')
        response.delete_cookie('sessionid')
        return response
