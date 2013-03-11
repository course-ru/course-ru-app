from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from main.models import *

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Feedback)

admin.site.unregister(User)

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)
