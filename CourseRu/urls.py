from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^', include('main.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^student/', include('student.urls')),
                       url(r'^instructor/', include('instructor.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))