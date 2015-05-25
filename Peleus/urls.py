from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import forecast.views as views

admin.autodiscover()
urlpatterns = patterns('',
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(template_name='index_page.html'), name='home'),
                       url(r'signup/$$', views.SignUpView.as_view(), name='signup'),
                       url(r'signup_last/$', views.SignUpSecondView.as_view(), name='signup2'),
                       url(r'login/$', views.LoginView.as_view(), name='login'),
                       url(r'logout/$', views.LogoutView.as_view(), name='logout'),
                       url(r'profile/$', TemplateView.as_view(template_name='profile_page.html'), name='profile'),

                       )
