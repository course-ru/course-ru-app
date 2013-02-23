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

def index(request):
    return render(request, 'CourseRuApp/index.html', {})

def courseList(request):
    courseList = Course.objects.all()
    return render(request, 'CourseRuApp/courselist.html', {'CourseList': courseList})

@login_required
def course(request, courseId):
    course = get_object_or_404(Course, pk=courseId)
    courseOfferingList = course.courseoffering_set.all()
    return render(request, 'CourseRuApp/course.html', {'Course': course, 'CourseOfferingList': courseOfferingList})

@login_required
def courseOffering(request, courseId, courseOfferingId):
    course = get_object_or_404(Course, pk=courseId)
    courseOffering = get_object_or_404(CourseOffering, pk=courseOfferingId)
    return render(request, 'CourseRuApp/courseoffering.html', {'Course': course, 'CourseOffering': courseOffering})

@login_required
def personal(request, userId):
    user = get_object_or_404(User, pk=userId)
    userProfile = user.userprofile
    return render(request, 'CourseRuApp/personal.html', {'User': user, 'UserProfile': userProfile})

@login_required
def addCourse(request):
    return render(request, 'CourseRuApp/addcourse.html', {})

@login_required
def addCourseOffering(request, courseId):
    course = get_object_or_404(Course, pk=courseId)
    return render(request, 'CourseRuApp/addcourseoffering.html', {'Course': course})
