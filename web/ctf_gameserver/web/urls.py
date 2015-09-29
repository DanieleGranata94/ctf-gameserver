from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .registration import views as registration_views
from .registration.forms import TeamAuthenticationForm, FormalPasswordResetForm

# pylint: disable=invalid-name, bad-continuation


# Arguments for the django.contrib.auth.views.password_reset view
_password_reset_args = {
    'template_name': 'password_reset.html',
    'email_template_name': 'password_reset_mail.txt',
    'subject_template_name': 'password_reset_subject.txt',
    'password_reset_form': FormalPasswordResetForm,
}


urlpatterns = [
    url(r'^register/$',
        registration_views.register,
        name='register'
    ),    # noqa
    url(r'^confirm/$',
        registration_views.confirm_email,
        name='confirm_email'
    ),

    url(r'^login/$',
        auth_views.login,
        {'template_name': 'login.html', 'authentication_form': TeamAuthenticationForm},
        name='login'
    ),
    url(r'^logout/$',
        auth_views.logout,
        # TODO
        {'next_page': '/'},
        name='logout'
    ),
    url(r'^reset-password/$',
        auth_views.password_reset,
        _password_reset_args,
        name='password_reset'
    ),
    url(r'^reset-password/done/$',
        auth_views.password_reset_done,
        {'template_name': 'password_reset_done.html'},
        name='password_reset_done'
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'
    ),

    url(r'^reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'
    ),

    url(r'^admin/', include(admin.site.urls))
]