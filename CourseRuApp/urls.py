from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('CourseRuApp.views',
    url(r'^$', 'index', name='index'),
    url(r'^addcourse/$', 'addCourse', name='addCourse'),
    url(r'^courses/(?P<courseId>\d+)/$', 'course', name='course'),
    url(r'^courses/(?P<courseId>\d+)/addcourseoffering/$', 'addCourseOffering', name='addCourseOffering'),
    url(r'^courses/(?P<courseId>\d+)/(?P<courseOfferingId>\d+)/$', 'courseOffering', name='courseOffering'),
    url(r'^courses/(?P<courseId>\d+)/(?P<courseOfferingId>\d+)/apply/$', 'courseOfferingApply', name='courseOfferingApply'),
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))