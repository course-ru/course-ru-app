from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import utc
from django.utils.datetime_safe import datetime
from main.models import *

denied = '/templates/denied/'

@permission_required('main.can_apply', login_url='/accounts/login')
def apply_for_course(request, course_id):
    user_profile = request.user.userprofile
    if len(user_profile.courses.filter(id=course_id)) == 0:
        course = get_object_or_404(Course, pk=course_id)
        user_profile.courses.add(course)
        user_profile.save()
        return HttpResponseRedirect(reverse('student.views.course', kwargs={'course_id': course_id}))
    else:
        return HttpResponseRedirect(reverse('student.views.course', kwargs={'course_id': course_id}))


@login_required
def course(request, course_id, template_name='student/course.html'):
    if len(request.user.userprofile.courses.filter(pk=course_id)) > 0:
        course = get_object_or_404(Course, id=course_id)
        documents = Document.objects.filter(course=course).filter(appear_date__lte=datetime.utcnow().replace(tzinfo=utc)).order_by('appear_date')
        return render(request, template_name, {'course': course, 'documents': documents})
    else:
        return HttpResponseRedirect(reverse('main.views.course', kwargs={'course_id': course_id}))


@login_required
def courses(request, template_name='student/courses.html'):
    courses = request.user.userprofile.courses.all()
    return render(request, template_name, {'Courses': courses})
