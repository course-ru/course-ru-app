# coding=utf-8
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.forms import TextInput
from django.utils.http import int_to_base36
from django.template import Context, loader
from django.contrib.auth.models import Group
from django import forms
from django.core.mail import send_mail


class ExtendedAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ExtendedAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = u'Имя пользователя'
        self.fields['username'].widget.attrs['placeholder'] = u'Имя пользователя'
        self.fields['password'].label = u'Пароль'
        self.fields['password'].widget.attrs['placeholder'] = u'Пароль'


class UserCreationForm(forms.ModelForm):
    username = forms.RegexField(label='Username',
                                max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text='Required',
                                error_messages={'invalid': 'Letters or digits only'})
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password confirmation',
                                       widget=forms.PasswordInput,
                                       help_text='Enter password again')
    email = forms.EmailField(label='EMail',
                             max_length=75)
    email_confirm = forms.EmailField(label='Email confirmation',
                                     max_length=75,
                                     help_text='Account confirmation letter will be sent on this email address')

    choices = [('Student', 'Student'),
               ('Teacher', 'Teacher')]

    role = forms.ChoiceField(choices=choices, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username',)

    def clean_role(self):
        choice = self.cleaned_data['role']
        if not (choice in [item[0] for item in self.choices]):
            raise forms.ValidationError('Unknown role')
        return choice

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password', '')
        password_confirm = self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

        return password_confirm

    def clean_email(self):
        email = self.cleaned_data['email']
        users_found = User.objects.filter(email__iexact=email)

        if len(users_found) >= 1:
            raise forms.ValidationError('Address already in use by another user')

        return email

    def clean_email_confirm(self):
        email = self.cleaned_data.get('email', '')
        email_confirm = self.cleaned_data['email_confirm']

        if email != email_confirm:
            raise forms.ValidationError('Emails do not match')

        return email_confirm

    def save(self, commit=True, domain_override=None, email_template_name='accounts/signup_email.html', use_https=False,
             token_generator=default_token_generator):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        choice = self.cleaned_data['role']
        user.is_active = False

        if commit:
            user.save()

            # save user group
            if choice == self.choices[0][0]:  # student
                group = Group.objects.get(name='Students')
            else:  # teacher
                group = Group.objects.get(name='Teachers')
            group.user_set.add(user)

        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        template = loader.get_template(email_template_name)
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
        }
        send_mail('Confirmation link sent on %s' % site_name,
                  template.render(Context(context)), 'courseru@gmail.com', [user.email])

        return user