"""myFirstDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from webchat import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

#https://docs.djangoproject.com/en/4.0/topics/http/urls/
urlpatterns = [


    path('', views.home, name='home'),#default home page path
    path('home/', views.home, name='home'),
    re_path(r'^signup/$',accounts_views.signup, name='signup'),
    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),

    re_path(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),

    re_path(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),

    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    #     name='password_reset_confirm'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
            name='password_reset_confirm'),

    re_path(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    #user changed password url
    re_path(r'^settings/password/$',
            auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
            name='password_change'),
    re_path(r'^settings/password/done/$',
            auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
            name='password_change_done'),

    re_path(r'^board_topic/(?P<pk>\d+)/$', views.board_topic, name='board_topic'),
    re_path(r'^board_topic/(?P<pk>\d+)/new/$', views.new_board_topic, name='new_board_topic'),
    path('admin/', admin.site.urls),

]
