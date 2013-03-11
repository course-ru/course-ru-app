from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import AddCourseForm
from main.models import *


denied = '/templates/denied/'


@permission_required('main.add_course', login_url=denied)
def add_course(request, template_name='instructor/addcourse.html', add_course_form=AddCourseForm,
               post_course_new_redirect=None):
    if request.method == 'POST':
        form = add_course_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_course_new_redirect is None:
                post_course_new_redirect = reverse('main.views.course', kwargs={'course_id': course.id})
            return HttpResponseRedirect(post_course_new_redirect)
    else:
        form = add_course_form()
    return render(request, template_name, {'form': form})


@login_required
def course(request, course_id, template_name='instructor/course.html'):
    if len(request.user.userprofile.courses.filter(pk=course_id)) > 0:
        course = get_object_or_404(Course, id=course_id)
        return render(request, template_name, {'course': course})
    else:
        return HttpResponseRedirect(reverse('main.views.course', kwargs={'course_id': course_id}))


@login_required
def courses(request, template_name='instructor/courses.html'):
    courses = request.user.userprofile.courses.all()
    return render(request, template_name, {'Courses': courses})
