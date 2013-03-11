# coding=utf-8
from django import forms
from django.forms import ModelForm
from main.models import *


class AddCourseForm(ModelForm):
    class Meta:
        model = Course

    def clean_name(self):
        name = self.cleaned_data['name']
        courses_found = Course.objects.filter(name__iexact=name)

        if len(courses_found) >= 1:
            raise forms.ValidationError('Name already in use in another course')

        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def save(self, commit=True):
        course = super(AddCourseForm, self).save(commit=False)
        course.name = self.cleaned_data['name']
        course.description = self.cleaned_data['description']
        course.start_date = self.cleaned_data['start_date']
        course.end_date = self.cleaned_data['end_date']
        course.organization = self.cleaned_data['organization']
        course.short_summary = self.cleaned_data['short_summary']
        course.logo = self.cleaned_data['logo']

        print course.logo

        if commit:
            course.save()

        return course


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = u'Текст сообщения'
        self.fields['body'].widget.attrs = {'rows': 6, 'class': 'span6', 'placeholder': u'Текст сообщения'}

    class Meta:
        model = Feedback