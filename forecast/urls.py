from django.conf.urls import patterns, include, url
from django.contrib import admin

import app.views as appviews

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', appviews.IndexView.as_view(), name="index"),
                       url(r'^sign_in/$', appviews.SignInView.as_view(), name="authorize"),
                       url(r'^sign_up/$', appviews.SignUpView.as_view(), name="signup"),
                       
                       url(r'^email_confirm/(?P<token>[A-Za-z0-9]{64})', appviews.EmailConfirmationView.as_view(),
                           name='email_confirmation'),
                       url(r'^thanx/(?P<token>[a-f0-9]+)/$', appviews.RegisteredView.as_view(), name="registered"),
                       url(r'^view_user/(?P<user_id>[0-9]{1,3})/$', appviews.UserView.as_view(), name="user"),
                       url(r'^profile/$', appviews.ProfileView.as_view(), name="profile"),
                       url(r'^forecast/$', appviews.ForecastView.as_view(), name="forecast"),
                       url(r'^organization/$', appviews.OrganizationView.as_view(), name="organization"),
                       url(r'^active_forecasts/$', appviews.ActiveForecastsView.as_view(), name="active_forecasts"),
                       url(r'^create_organization/$', appviews.CreateOrganizationView.as_view(),
                           name="create_organization"),
                       url(r'^create_forecast/$', appviews.CreateForecastView.as_view(), name="create_forecast"),
                       url(r'^submit_forecast/$', appviews.ForecastView.as_view(), name="submit_forecast"),
                       url(r'^logout/$', appviews.LogoutView.as_view(), name="logout"),
)
