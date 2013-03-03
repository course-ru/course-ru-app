from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import *

denied = '/templates/denied/'


def index(request, template_name='main/index.html'):
    courses = Course.objects.all().order_by('start_date')
    return render(request, template_name, {'courses': courses})


def about(request, template_name='main/about.html'):
    return render(request, template_name)


def course(request, course_id, template_name='main/course.html'):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, template_name, {'course': course})