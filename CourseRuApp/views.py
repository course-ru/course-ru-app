from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import RequestContext
from django.conf import settings
from django.db import connection

def index(request):
    if request.user.is_authenticated():
        return HttpResponse('HUJ')
    else:
        return HttpResponse('NE HUJ')

def courseList(request):
    return HttpResponse('List')

def courseOne(request, courseId):
    return HttpResponse('Course #'+str(courseId))

def courseOffering(request, courseId, courseOfferingId):
    return HttpResponse('CourseOffering #'+str(courseId)+'/'+str(courseOfferingId))