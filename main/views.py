# coding=utf-8
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render_to_response
from django.template.defaultfilters import default_if_none
from main.forms import FeedbackForm
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


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('main.views.index')
    else:
        form = FeedbackForm()

    return render(request, 'main/feedback.html', {
        'form': form,
    })