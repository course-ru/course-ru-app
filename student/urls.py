from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('student.views',
                       url(r'^courses/(?P<course_id>\d+)/apply/$', 'apply_for_course', name='apply_for_course'),
                       url(r'^courses/(?P<course_id>\d+)/$', 'course', name='course'),
                       url(r'^courses/$', 'courses', name='courses')
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))