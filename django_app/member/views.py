from .models import MyUser
from .serializers import MyUserserializer
from rest_framework import generics


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserserializer