import json
from datetime import datetime, date
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _

from forms import UserRegistrationForm, SignupCompleteForm, CustomUserProfile
from models import Forecast
from Peleus.settings import APP_NAME,\
    FORECAST_FILTER_MOST_ACTIVE, FORECAST_FILTER_NEWEST, FORECAST_FILTER_CLOSING


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class ActiveForecastsView(View):
    template_name = ''

    def get(self, request):
        return render(request, self.template_name)


class ActiveForecastVoteView(View):
    def post(self, request):
        data = request.POST


class EmailConfirmationView(View):
    template_name = 'email_confirm_page.html'

    def get(self, request):
        token = request.GET.get('token')
        res_dict = dict()
        try:
            user = CustomUserProfile.objects.get(activation_token=token)
        except User.DoesNotExist as ex:
            res_dict['error'] = ex
            return render(request, self.template_name, res_dict)
        if token == user.customuserprofile.activation_token and datetime.now() <= user.customuserprofile.expires_at:
            user.email_verified = True
            res_dict['success'] = _('Email was verified!')
            user.save()
        else:
            res_dict['error'] = _('Provided token is incorrect or expired')
        return render(request, self.template_name, res_dict)


class ForecastsJsonView(View):

    def get(self, request):
        data = request.GET
        list_ids = data.getlist('ids')

    def _queryset_by_forecast_filter(self, forecasts, forecast_filter):
        if forecast_filter == FORECAST_FILTER_MOST_ACTIVE:
            forecasts = forecasts.annotate(num_votes=Count('votes')).order_by('-num_votes')
        elif forecast_filter == FORECAST_FILTER_NEWEST:
            forecasts = forecasts.annotate(num_votes=Count('votes')).order_by('-start_date')
        elif forecasts == FORECAST_FILTER_CLOSING:
            forecasts = forecasts.oreder_by('-end_date')
        return forecasts

    def _respond(self, forecasts):
        return HttpResponse(json.dumps([f.to_json() for f in forecasts]),
                            content_type='application/json')


class LoginView(View):
    def post(self, request):
        request.session.set_test_cookie()
        if not request.session.test_cookie_worked():
            return HttpResponse(_("Please enable cookies and try again."))
        request.session.delete_test_cookie()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:  # and user.is_active:
            login(request, user)
            try:
                if not user.customuserprofile.conditions_accepted:
                    return HttpResponseRedirect(reverse('signup2'))
            except Exception:
                pass
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse(_('Invalid login or password'), status=400)


class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return HttpResponseRedirect(reverse('home'))


class SignUpView(View):
    template_name = 'sign_up_page.html'
    error_template = 'error_login_page.html'
    form = UserRegistrationForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form, 'app_name': APP_NAME })

    def post(self, request):
        signup_form = UserRegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            request.session['uid'] = user.id
            return HttpResponseRedirect(reverse('signup2'))
        else:
            return render(request, self.error_template, {'errors': signup_form.errors})


class SignUpSecondView(View):
    template_name = 'sign_up2_page.html'
    form = SignupCompleteForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user_id = request.session['uid']
            user_profile = CustomUserProfile.objects.get(user=user_id)
            user_profile.conditions_accepted = True
            user_profile.save()
            form.save(user_id)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('errors'))
