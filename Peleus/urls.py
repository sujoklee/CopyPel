from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.views.generic import TemplateView

import forecast.views as views
from Peleus.settings import MEDIA_ROOT

admin.autodiscover()
urlpatterns = patterns(
    '',
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'about/$', TemplateView.as_view(template_name='about_page.html'), name='about'),
    url(r'^$', views.IndexPageView.as_view(), name='home'),
    url(r'profile/$', TemplateView.as_view(template_name='profile_page.html'), name='profile'),
    url(r'signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'signuplast/$', views.SignUpSecondView.as_view(), name='signup2'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^errors/$', TemplateView.as_view(template_name='error_login_page.html'), name='errors'),
    url(r'^active_forecasts/$', views.ActiveForecastsView.as_view(), name='active_forecasts'),
    url(r'^archived_forecasts/$', views.ArchivedForecastsView.as_view(), name='archived_forecasts'),
    url(r'^propose_forecast/$', views.ProposeForecastView.as_view(), name='propose_forecast'),
    url(r'^forecast/(?P<id>\d+)/$', views.IndividualForecastView.as_view(), name='individual_forecast'),
    url(r'^forecasts/$', views.ForecastsJsonView.as_view(), name='forecasts'),
    url(r'^forecast_vote/$', views.ActiveForecastVoteView.as_view(), name='forecast_vote')
) + static.static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
