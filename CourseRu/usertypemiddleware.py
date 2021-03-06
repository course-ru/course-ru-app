from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from re import compile

STUDENT_URLS = [compile(r'^student/')]
INSTRUCTOR_URLS = [compile(r'^instructor/')]
URLS = INSTRUCTOR_URLS + STUDENT_URLS

class UserTypeMiddleware:

    def process_request(self, request):
        path = request.path_info.lstrip('/')
        if request.user.is_authenticated():
            if not request.user.is_superuser:
                if request.user.userprofile.is_student():
                    if any(m.match(path) for m in INSTRUCTOR_URLS):
                        return HttpResponseRedirect(reverse('accounts.views.denied'))
                if request.user.userprofile.is_instructor():
                    if any(m.match(path) for m in STUDENT_URLS):
                        return HttpResponseRedirect(reverse('accounts.views.denied'))
        else:
            if any(m.match(path) for m in URLS):
                return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
