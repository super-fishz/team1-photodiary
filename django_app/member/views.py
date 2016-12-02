from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserserializer



class CurrentUserDetail(APIView):
    def get(self, request):
        user = self.request.user
        serializer = MyUserserializer(user)
        return Response(serializer.data)