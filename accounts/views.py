# coding=utf-8
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from accounts.forms import UserCreationForm


@csrf_protect
def signup(request, template_name='templates/signup.html', email_template_name='templates/signup_email.html',
           signup_form=UserCreationForm, token_generator=default_token_generator, post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('index')

    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name

            if not Site._meta.installed:
                opts['domain_override'] = RequestSite(request).domain

            form.save(**opts)
            messages.info(request, 'На указанный адрес электронной почты отправлено письмо с дальнейшими инструкциями')
            return HttpResponseRedirect(post_signup_redirect)

    else:
        form = signup_form()

    return render(request, template_name, {'form': form})


def signup_confirm(request, uidb36=None, token=None, token_generator=default_token_generator,
                   post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('index')

    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()

    else:
        context_instance['validlink'] = False

    messages.success(request, 'Регистрация успешно завершена')
    return HttpResponseRedirect(post_signup_redirect)


def profile(request):
    user = request.user
    user_profile = user.userprofile
    user_courses = user_profile.courses.all()
    return render(request, {'user': user, 'user_profile': user_profile, 'courses': user_courses})


def denied(request, template_name='templates/noaccess.html'):
    return render(request, template_name)


def init(request):
    # temp. version
    #
    students_group, created = Group.objects.get_or_create(name='Students')
    students_group.permissions.add(Permission.objects.get(codename='can_apply'))
    teachers_group, created = Group.objects.get_or_create(name='Teachers')
    teachers_group.permissions.add(Permission.objects.get(codename='add_course'))
    return HttpResponse('Groups have been initialized')