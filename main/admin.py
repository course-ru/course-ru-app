from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from main.models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'users'' profiles'


class UserAdmin(UserAdmin):
    users_profiles = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Feedback)