from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create/$', CreateUser.as_view()),
    url(r'^detail/$', DetailUser.as_view()),
    url(r'^reset_password/$', DetailUser.as_view()),
    url(r'^login/$', Login_ObtainAuthToken.as_view()),
    url(r'^logout/$', Logout_RemoveAuthToken.as_view()),
    url(r'^alluser/$', CreateUser.as_view())
]
