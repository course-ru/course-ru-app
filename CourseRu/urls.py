from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^about/', 'main.views.about', name='about'),
                       url(r'^main/', include('main.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)