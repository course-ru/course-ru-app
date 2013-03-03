from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import AddCourseForm

denied = '/templates/denied/'


@permission_required('main.add_course', login_url=denied)
def add_course(request, template_name='main/add_course.html', add_course_form=AddCourseForm,
               post_course_new_redirect=None):
    if request.method == 'POST':
        form = add_course_form(request.POST)
        if form.is_valid():
            course = form.save()
            if post_course_new_redirect is None:
                post_course_new_redirect = reverse('main.views.course', kwargs={'courseId': course.id})
            return HttpResponseRedirect(post_course_new_redirect)
    else:
        form = add_course_form()
    return render(request, template_name, {'form': form})