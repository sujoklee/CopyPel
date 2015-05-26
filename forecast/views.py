import json
from datetime import date

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

from forms import UserRegistrationForm, SignupCompleteForm, CustomUserProfile
from models import Forecast
from Peleus.settings import APP_NAME,\
    FORECAST_FILTER_MOST_ACTIVE, FORECAST_FILTER_NEWEST, FORECAST_FILTER_CLOSING


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class EmailConfirmationView(View):
    template_name = 'email_confirm_page.html'

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


class ForecastsJsonView(View):

    def get(self, request):
        query = {'end_date__lt': date.today()}
        qs = Forecast.objects.all()

        if 'id' in request.GET:
            query['pk__in'] = request.GET.getlist('id')
            qs = qs.filter(**query)
            self._respond(qs)
        # elif 'name' in request.GET:
        #     query['forecast_question__in'] = request.GET.getlist('name')
        #     qs = Forecast.objects.filter(**query)
        else:
            forecast_filter = request.GET.get('filter', FORECAST_FILTER_MOST_ACTIVE)
            qs = self._queryset_by_forecast_filter(qs, forecast_filter)
        return self._respond(qs)

    def _queryset_by_forecast_filter(self, forecasts, forecast_filter):
        if forecast_filter == FORECAST_FILTER_MOST_ACTIVE:
            forecasts = forecasts.annotate(num_votes=Count('votes')).order_by('-num_votes')
        elif forecast_filter == FORECAST_FILTER_NEWEST:
            forecasts = forecasts.order_by('-start_date')
        elif forecasts == FORECAST_FILTER_CLOSING:
            forecasts = forecasts.oreder_by('-end_date')
        return forecasts

    def _respond(self, forecasts):
        # forecasts = Forecast.objects.all().prefetch_related()
        return HttpResponse(json.dumps([f.to_json() for f in forecasts]),
                            content_type='application/json')


class LoginView(View):
    def post(self, request):
        request.session.set_test_cookie()
        if not request.session.test_cookie_worked():
            return HttpResponse("Please enable cookies and try again.")
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
            return HttpResponse('Invalid login or password', status=400)


class LogoutView(View):
    def get(self, request):
        response = logout(request)
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
            signup_form.save()
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
            user = request.user
            user.customuserprofile.conditions_accepted = True
            user.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('errors'))
