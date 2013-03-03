from django.conf.urls import patterns, include, url

urlpatterns = patterns('instructor.views',
                       url(r'^courses/new/$', 'add_course', name='add_course'),
                       )