from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from accounts.views import *
from main.models import *
from main.forms import *

denied = '/accounts/denied/'


def index(request, template_name='main/index.html'):
    courseList = Course.objects.all()
    return render(request, template_name, {'CourseList': courseList})


def about(request, template_name='main/about.html'):
    return render(request, template_name)


@login_required
def course(request, courseId, template_name='main/course.html'):
    course = get_object_or_404(Course, pk=courseId)
    courseOfferingList = course.courseoffering_set.all()
    return render(request, template_name, {'Course': course, 'CourseOfferingList': courseOfferingList})


@login_required
def courseOffering(request, courseId, courseOfferingId, template_name='main/courseoffering.html'):
    course = get_object_or_404(Course, pk=courseId)
    courseOffering = get_object_or_404(CourseOffering, pk=courseOfferingId)
    onCourse = True if (len(request.user.userprofile.courses.filter(id=courseOfferingId)) > 0) else False
    return render(request, template_name, {'Course': course, 'CourseOffering': courseOffering, 'OnCourse': onCourse})


@login_required
def profile(request, userId, template_name='main/profile.html'):
    user = get_object_or_404(User, pk=userId)
    userProfile = user.userprofile
    return render(request, template_name, {'User': user, 'UserProfile': userProfile})


@permission_required('main.add_course', login_url=denied)
def addCourse(request, template_name='main/addcourse.html', addcourse_form=AddCourseForm, post_addcourse_redirect=None):
    if request.method == 'POST':
        form = addcourse_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_addcourse_redirect is None:
                post_addcourse_redirect = reverse('main.views.course', kwargs={'courseId': course.id})
            return HttpResponseRedirect(post_addcourse_redirect)
    else:
        form = addcourse_form()
    return render(request, template_name, {'form': form})


@permission_required('main.add_courseoffering', login_url=denied)
def addCourseOffering(request, courseId, addcourseoffering_form=AddCourseOfferingForm,
                      template_name='main/addcourseoffering.html', post_addcourseoffering_redirect=None):
    course = get_object_or_404(Course, pk=courseId)
    if request.method == 'POST':
        form = addcourseoffering_form(request.POST)
        if form.is_valid():
            courseOffering = form.save()
            course = courseOffering.course
            if post_addcourseoffering_redirect is None:
                post_addcourseoffering_redirect = reverse('main.views.courseOffering', kwargs={'courseId': course.id,
                                                                                               'courseOfferingId': courseOffering.id})
            return HttpResponseRedirect(post_addcourseoffering_redirect)
    else:
        form = addcourseoffering_form(initial={'course': course})
    return render(request, template_name, {'form': form})


@permission_required('main.can_apply', login_url=denied)
def courseOfferingApply(request, courseId, courseOfferingId):
    userProfile = request.user.userprofile
    userCourseOfferings = userProfile.courses.filter(id=courseOfferingId)
    courseOffering = get_object_or_404(CourseOffering, pk=courseOfferingId)
    if len(userCourseOfferings) == 0:
        userProfile.courses.add(courseOffering)
        userProfile.save()
    return HttpResponseRedirect(
        reverse('main.views.courseOffering', kwargs={'courseId': courseId, 'courseOfferingId': courseOfferingId}))

