from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from main.models import *


class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'short_summary', 'description', 'organisation', 'logo', 'start_date', 'end_date']
    list_display = ('name', 'short_summary', 'description', 'organisation', 'logo', 'start_date', 'end_date')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'users'' profiles'


class UserAdmin(UserAdmin):
    users_profiles = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)


name = models.CharField(max_length=100)
short_summary = models.TextField(blank=True)
description = models.TextField()
organisation = models.CharField(max_length=100)
logo = models.FileField(upload_to='logos')
start_date = models.DateField()
end_date = models.DateField()