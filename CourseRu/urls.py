from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^main/', include('main.urls')),
                       url(r'^account/', include('account.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)