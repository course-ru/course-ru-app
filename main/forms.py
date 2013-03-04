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
        if commit:
            course.save()
        return course


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback