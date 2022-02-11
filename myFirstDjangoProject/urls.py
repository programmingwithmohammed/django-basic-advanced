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

#https://docs.djangoproject.com/en/4.0/topics/http/urls/
urlpatterns = [

    #path('homepage/', views.homepage, name='homepage'),
    path('', views.home, name='home'),#default home page path
    path('home/', views.home, name='home'),

    #path('board_topic/', views.board_topic, name='board_topic'),
    re_path(r'^board_topic/(?P<pk>\d+)/$', views.board_topic, name='board_topic'),
    re_path(r'^board_topic/(?P<pk>\d+)/new/$', views.new_board_topic, name='new_board_topic'),

# =============================================================================
#     path('about/', views.about, name='about'),
#     path('about/comapny', views.about_company, name='about_comapny'),
#     path('about/author', views.about_author, name='about_author'),
#     path('about/privacy', views.about_privacy, name='about_privacy'),
# =============================================================================

    #path('(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile')



    path('admin/', admin.site.urls),

]

#url writing convention
#def url(regex, view, kwarg=None, name=None):
#http://127.0.0.1:8000/chatboard/?page=5 only/chat_topic