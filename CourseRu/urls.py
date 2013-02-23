from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^CourseRuApp/', include('CourseRuApp.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
