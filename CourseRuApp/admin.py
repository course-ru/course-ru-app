from CourseRuApp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name', 'description')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)

