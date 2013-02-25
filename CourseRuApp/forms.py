from django import forms
from CourseRuApp.models import *
from django.forms import ModelForm

class AddCourseForm(ModelForm):

    class Meta:
        model = Course

    def name_clean(self):
        name = self.cleaned_data['name']
        courses_found = Course.objects.filter(name__iexact=name)

        if len(courses_found) >= 1:
            raise forms.ValidationError('Name already in use in another course')

        return name


    def description_clean(self):
        description = self.cleaned_data['description']
        return description


    def save(self, commit=True):
        course = super(AddCourseForm, self).save(commit=False)
        course.name = self.cleaned_data['name']
        course.description = self.cleaned_data['description']
        course.save()
        return course

class AddCourseOfferingForm(ModelForm):
    class Meta:
        model = CourseOffering