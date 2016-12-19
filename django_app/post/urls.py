"""photodiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from post import views
from .views import *

urlpatterns = [
    url(r'^$', PostList.as_view()),
    url(r'^(?P<post_pk>[0-9]+)/$', PostDetail.as_view()),
    url(r'^search/$', PostTitleSearch.as_view()),
    url(r'^(?P<post_pk>[0-9]+)/photo/$', PhotoDetail.as_view()),
    url(r'^(?P<post_pk>[0-9]+)/photo/(?P<photo_pk>[0-9]+)/$', PhotoDetail.as_view()),
    url(r'^today-photo/create/$', CreateTodayPhoto.as_view()),
    url(r'^today-photo/get-3/$', PickTodayPhoto.as_view()),
    url(r'^today-photo/get-3/(?P<select_id>[0-9]+)/$', PickTodayPhoto.as_view()),
    url(r'^make-zip/$', ZipAndSendMail.as_view()),
]
