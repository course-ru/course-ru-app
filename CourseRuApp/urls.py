from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('CourseRuApp.views',
    url(r'^$', 'index'),
    url(r'^courses/$', 'courseList'),
    url(r'^courses/(?P<courseId>\d+)/$', 'courseOne'),
    url(r'^courses/(?P<courseId>\d+)/(?P<courseOfferingId>\d+)/$', 'courseOffering'),
##    url(r'^$', 'index'),
##    url(r'^upload/', 'upload'),
##    url(r'^import/', 'base'),
##    url(r'^list/$', 'list', name='list'),
##    url(r'^list/(?P<docid>\d+)/$', 'show'),
##    url(r'^test/$', 'test')
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))