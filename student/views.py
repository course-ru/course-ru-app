from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from main.models import Course

denied = '/templates/denied/'


@permission_required('main.can_apply', login_url='/accounts/login?huy=pizda')
def apply_for_course(request, course_id):
    user_profile = request.user.userprofile
    if len(user_profile.courses.filter(id=course_id)) == 0:
        course = get_object_or_404(Course, pk=course_id)
        user_profile.courses.add(course)
        user_profile.save()
        return HttpResponseRedirect(reverse('course', kwargs={'courseId': course_id}))
    else:
        return HttpResponseRedirect(reverse('course', kwargs={'courseId': course_id}))


def course(request, course_id, template_name='student/course.html'):
    course = get_object_or_404(Course, id=course_id)
    return render(request, template_name, {'course': course})