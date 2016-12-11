from django.conf.urls import url, include
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^create/$', CreateUser.as_view()),
    url(r'^detail/$', DetailUser.as_view()),
    url(r'^login/$', Login_ObtainAuthToken.as_view()),
    url(r'^logout/$', Logout_RemoveAuthToken.as_view())
]
