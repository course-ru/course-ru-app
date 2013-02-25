from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^CourseRuApp/', include('CourseRuApp.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

#
# That's strange, but groups are getting initialized here
# Trying to find better solution
#
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
students_group, created = Group.objects.get_or_create(name='Students')
students_group.permissions.add(Permission.objects.get(codename='can_apply'))
teachers_group, created = Group.objects.get_or_create(name='Teachers')
teachers_group.permissions.add(Permission.objects.get(codename='add_course'))
teachers_group.permissions.add(Permission.objects.get(codename='add_courseoffering'))