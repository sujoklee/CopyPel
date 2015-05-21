from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import forecast.views as views

admin.autodiscover()
urlpatterns = patterns('',
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(template_name='index_page.html'), name='home'),
                       url(r'signup$', views.SignUpView.as_view(), name='signup'),
                       url(r'signup2$', views.SignUpSecondView.as_view(), name='signup2')

                       )
