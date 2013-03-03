from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from accounts.views import *
from main.models import *
from main.forms import *

denied = '/templates/denied/'


def index(request, template_name='main/index.html'):
    courses = Course.objects.all()
    return render(request, template_name, {'courses': courses})


def about(request, template_name='main/about.html'):
    return render(request, template_name)


@login_required
def course(request, course_id, template_name='main/course.html'):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, template_name, {'course': course})


@login_required
def profile(request, user_id, template_name='main/profile.html'):
    user = get_object_or_404(User, pk=user_id)
    user_profile = user.userprofile
    return render(request, template_name, {'User': user, 'UserProfile': user_profile})


@permission_required('main.can_add_course', login_url=denied)
def add_course(request, template_name='main/add_course.html', add_course_form=AddCourseForm,
               post_course_new_redirect=None):
    if request.method == 'POST':
        form = add_course_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_course_new_redirect is None:
                post_course_new_redirect = reverse('main.views.course', kwargs={'courseId': course.id})
            return HttpResponseRedirect(post_course_new_redirect)
    else:
        form = add_course_form()
    return render(request, template_name, {'form': form})


@permission_required('main.can_apply_for_course', login_url=denied)
def apply_for_course(request, course_id):
    user_profile = request.user.userprofile
    if len(user_profile.courses.filter(id=course_id)) == 0:
        course = get_object_or_404(Course, pk=course_id)
        user_profile.courses.add(course)
        user_profile.save()

    return HttpResponseRedirect(reverse('main.views.course', kwargs={'courseId': course_id}))

