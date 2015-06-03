import json
from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from forms import UserRegistrationForm, SignupCompleteForm, CustomUserProfile, ForecastForm, ForecastVoteForm
from models import Forecast, ForecastPropose, ForecastVotes
from Peleus.settings import APP_NAME,\
    FORECAST_FILTER_MOST_ACTIVE, FORECAST_FILTER_NEWEST, FORECAST_FILTER_CLOSING


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class ActiveForecastsView(View):
    template_name = 'forecasts_page.html'

    def get(self, request):
        forecasts = Forecast.objects.all()
        return render(request, self.template_name, {'data': forecasts, 'is_active': True})


class ActiveForecastVoteView(View):
    def post(self, request):
        data = request.POST
        forecast_id = data.get('forecast-id', None)
        vote = data.get('forecast-vote', None)
        if not forecast_id and not vote:
            return HttpResponseRedirect(reverse('home'))
        forecast = Forecast.objects.get(pk=forecast_id)
        todays_vote = forecast.votes.filter(date=date.today(), user_id=request.user)
        if todays_vote.count() == 0:
            forecast.votes.create(user_id=request.user, vote=vote, date=date.today())
        else:
            todays_vote.update(vote=vote)

        return HttpResponseRedirect(reverse('individual_forecast', kwargs={'id': forecast_id}))


class ArchivedForecastsView(View):
    template_name = 'forecasts_page.html'

    def get(self, request):
        forecasts = Forecast.objects.all()
        return render(request, self.template_name, {'data': forecasts, 'is_active': False})


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
        qs = Forecast.objects.all()

        if 'id' in request.GET:
            qs = qs.filter(pk__in=request.GET.getlist('id'))
            self._respond(qs)
        # elif 'name' in request.GET:
        #     query['forecast_question__in'] = request.GET.getlist('name')
        #     qs = Forecast.objects.filter(**query)
        else:
            qs = Forecast.objects.filter(end_date__gte=date.today())
            forecast_filter = request.GET.get('filter', FORECAST_FILTER_MOST_ACTIVE)
            qs = self._queryset_by_forecast_filter(qs, forecast_filter)
        return self._respond(qs)

    def _queryset_by_forecast_filter(self, forecasts, forecast_filter):
        if forecast_filter == FORECAST_FILTER_MOST_ACTIVE:
            forecasts = forecasts.annotate(num_votes=Count('votes')).order_by('-num_votes')
        elif forecast_filter == FORECAST_FILTER_NEWEST:
            forecasts = forecasts.annotate(num_votes=Count('votes')).order_by('-start_date')
        elif forecasts == FORECAST_FILTER_CLOSING:
            forecasts = forecasts.annotate(num_votes=Count('votes')).oreder_by('-end_date')
        return forecasts

    def _respond(self, forecasts):
        return HttpResponse(json.dumps([f.to_json() for f in forecasts]),
                            content_type='application/json')


class IndexPageView(View):
    template_name = 'index_page.html'

    def get(self, request):
        forecasts = Forecast.objects.all()
        return render(request, self.template_name, {'data': forecasts})


class IndividualForecastView(View):
    template_name = 'individual_forecast_page.html'

    def get(self, request, id):
        forecast = Forecast.objects.get(pk=id)
        voted_before = forecast.votes.filter()
        return render(request, self.template_name, {'forecast': forecast})


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


class PlaceVoteView(View):
    def post(self, request):
        data = request.POST
        user = request.user
        form = ForecastForm(data)
        if not form.is_valid():
            return HttpResponse(_('Invalid input data!'), status=400)
        forecast = get_object_or_404(Forecast, pk=data.get('fid'))
        f_vote = ForecastVotes.objects.filter(user_id__eq=user.id, forecast_id__eq=forecast.id)
        if f_vote:
            f_vote.update(vote=data.get('vote'))
            f_vote.save()
        else:
            new_f_vote = ForecastVotes(user_id=request.user, forecast_id=forecast, vote=data.get('vote'))
            new_f_vote.save()
        return HttpResponse('ok')


class ProposeForecastView(View):
    template_name = 'propose_forecast_page.html'
    form = ForecastForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        user = request.user
        form = self.form(request.POST)
        if form.is_valid():
            forecast_type_new = form.cleaned_data['forecast_type_new']
            forecast_question_new = form.cleaned_data['forecast_question_new']
            propose = ForecastPropose.objects.create(
                                        user_id=request.user,
                                        forecast_type_new = forecast_type_new,
                                        forecast_question_new = forecast_question_new
                                        )
            propose.save()
            return HttpResponse('Thank you for your forecast.')
        else:
            return render(request, self.template_name, {'form': form})


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
            user_id = request.session.get('uid') or request.user.id
            user_profile = CustomUserProfile.objects.get(user=user_id)
            user_profile.conditions_accepted = True
            user_profile.save()
            form.save(user_id)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('errors'))
