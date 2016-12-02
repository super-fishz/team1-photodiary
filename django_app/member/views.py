from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_auth.views import LoginView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from .models import MyUser
from .serializers import *
from rest_framework import generics


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserserializer