from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import MyUser
__all__ = [
    'UserList',
    'CurrentUserDetail'
    ]


class UserList(generics.ListCreateAPIView,
               generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        result = serializer.data
        result.pop('password')
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)




class CurrentUserDetail(APIView):
    def get(self, request):
        user = self.request.user
        serializer = MyUserSerializer(user)
        return Response(serializer.data)

