from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import forecast.views as views

admin.autodiscover()
urlpatterns = patterns(
    '',
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index_page.html'), name='home'),
    url(r'profile/$', TemplateView.as_view(template_name='profile_page.html'), name='profile'),
    url(r'signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'signuplast/$', views.SignUpSecondView.as_view(), name='signup2'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^errors/$', TemplateView.as_view(template_name='error_login_page.html'), name='errors'),
    url(r'^active_forecasts/$', views.ActiveForecastsView.as_view(), name='active_forecasts'),
    url(r'^archived_forecasts/$', views.ArchivedForecastsView.as_view(), name='archived_forecasts'),
    url(r'^forecasts/$', views.ForecastsJsonView.as_view(), name='forecasts'),
)
