# coding=utf-8
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from main.forms import FeedbackForm
from main.models import *

denied = '/templates/denied/'


def index(request):
    courses = Course.objects.all().order_by('start_date')
    return render(request, 'main/index.html', {'courses': courses})


def about(request):
    return render(request, 'main/about.html')


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'main/course.html', {'course': course})


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