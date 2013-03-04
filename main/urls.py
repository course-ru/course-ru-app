from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
                       url(r'^index/$', 'index'),
                       url(r'^about/$', 'about', name='about'),
                       url(r'^courses/(?P<course_id>\d+)/$', 'course', name='course'),
                       url(r'^feedback$', 'feedback', name='feedback'),
)