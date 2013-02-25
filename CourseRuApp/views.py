from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import RequestContext
from django.conf import settings
from django.db import connection
from django.contrib.auth.decorators import login_required
from CourseRuApp.models import *
from CourseRuApp.forms import *

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
    return render(request, template_name, {'Course': course, 'CourseOffering': courseOffering})

@login_required
def personal(request, userId, template_name='CourseRuApp/personal.html'):
    user = get_object_or_404(User, pk=userId)
    userProfile = user.userprofile
    return render(request, template_name, {'User': user, 'UserProfile': userProfile})

@login_required
def addCourse(request, template_name='CourseRuApp/addcourse.html', addcourse_form=AddCourseForm, post_addcourse_redirect=None):
    if request.method == 'POST':
        form = addcourse_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_addcourse_redirect is None:
                 post_addcourse_redirect = reverse('CourseRuApp.views.course', course.id)
            return HttpResponseRedirect(post_addcourse_redirect) # Redirect after POST
    else:
        form = addcourse_form()
    return render(request, template_name, {'form': form})


@login_required
def addCourseOffering(request, courseId, template_name='CourseRuApp/addcourseoffering.html'):
    course = get_object_or_404(Course, pk=courseId)
    return render(request, template_name, {'Course': course})
