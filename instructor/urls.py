from django.conf.urls import patterns, include, url

urlpatterns = patterns('instructor.views',
                       url(r'^courses/new/$', 'add_course', name='add_course'),
                       url(r'^courses/(?P<course_id>\d+)/$', 'course', name='course'),
                       url(r'^courses/$', 'courses', name='courses'),
                       url(r'^courses/(?P<course_id>\d+)/upload/$', 'upload', name='upload'),
                       )