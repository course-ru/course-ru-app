from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import RequestContext
from django.conf import settings
from django.db import connection
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from accounts.views import *
from CourseRuApp.models import *
from CourseRuApp.forms import *

denied = '/accounts/denied/'

def index(request, template_name='CourseRuApp/index.html'):
    return render(request, template_name, {})

def courseList(request, template_name='CourseRuApp/courselist.html'):
    courseList = Course.objects.all()
    return render(request, template_name, {'CourseList': courseList})

@login_required
def course(request, courseId, template_name='CourseRuApp/course.html'):
    course = get_object_or_404(Course, pk=courseId)
    courseOfferingList = course.courseoffering_set.all()
    return render(request, template_name, {'Course': course, 'CourseOfferingList': courseOfferingList})

@login_required
def courseOffering(request, courseId, courseOfferingId, template_name='CourseRuApp/courseoffering.html'):
    course = get_object_or_404(Course, pk=courseId)
    courseOffering = get_object_or_404(CourseOffering, pk=courseOfferingId)
    onCourse = True if (len(request.user.userprofile.courses.filter(id=courseOfferingId)) > 0) else False
    return render(request, template_name, {'Course': course, 'CourseOffering': courseOffering, 'OnCourse': onCourse})

@login_required
def personal(request, userId, template_name='CourseRuApp/personal.html'):
    user = get_object_or_404(User, pk=userId)
    userProfile = user.userprofile
    return render(request, template_name, {'User': user, 'UserProfile': userProfile})

@permission_required('CourseRuApp.add_course', login_url=denied)
def addCourse(request, template_name='CourseRuApp/addcourse.html', addcourse_form=AddCourseForm, post_addcourse_redirect=None):
    if request.method == 'POST':
        form = addcourse_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_addcourse_redirect is None:
                 post_addcourse_redirect = reverse('CourseRuApp.views.course', kwargs={'courseId': course.id})
            return HttpResponseRedirect(post_addcourse_redirect)
    else:
        form = addcourse_form()
    return render(request, template_name, {'form': form})

@permission_required('CourseRuApp.add_courseoffering', login_url=denied)
def addCourseOffering(request, courseId, addcourseoffering_form=AddCourseOfferingForm, template_name='CourseRuApp/addcourseoffering.html', post_addcourseoffering_redirect=None):
    course = get_object_or_404(Course, pk=courseId)
    if request.method == 'POST':
        form = addcourseoffering_form(request.POST)
        if form.is_valid():
            courseOffering = form.save()
            course = courseOffering.course
            if post_addcourseoffering_redirect is None:
                post_addcourseoffering_redirect = reverse('CourseRuApp.views.courseOffering', kwargs={'courseId': course.id, 'courseOfferingId': courseOffering.id})
            return HttpResponseRedirect(post_addcourseoffering_redirect)
    else:
        form = addcourseoffering_form(initial={'course': course})
    return render(request, template_name, {'form': form})

@permission_required('CourseRuApp.can_apply', login_url=denied)
def courseOfferingApply(request, courseId, courseOfferingId):
    userProfile = request.user.userprofile
    userCourseOfferings = userProfile.courses.filter(id=courseOfferingId)
    courseOffering = get_object_or_404(CourseOffering, pk=courseOfferingId)
    if len(userCourseOfferings) == 0:
        userProfile.courses.add(courseOffering)
        userProfile.save()
    return HttpResponseRedirect(reverse('CourseRuApp.views.courseOffering', kwargs={'courseId': courseId, 'courseOfferingId': courseOfferingId}))

