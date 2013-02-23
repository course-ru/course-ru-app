from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'Accounts/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'Accounts/logout.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'Accounts/password_change_form.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'Accounts/password_change_done.html'}),
    url(r'^signup/$', 'accounts.views.signup', {'template_name': 'Accounts/signup_form.html', 'email_template_name': 'Accounts/signup_email.html'}),
    url(r'^signup/done/$', 'accounts.views.signup_done', {'template_name': 'Accounts/signup_done.html'}),
    url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'accounts.views.signup_confirm'),
    url(r'^signup/complete/$', 'accounts.views.signup_complete', {'template_name': 'Accounts/signup_complete.html'}),
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))