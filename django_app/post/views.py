from django.http import HttpResponse
from rest_framework import generics
from .models import Photo, Post
from .serializers import Photoserializer, Postserializer
from member.models import MyUser
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView):
    serializer_class = Postserializer

    def get_queryset(self):
        print(self.request.user.pk)
        return self.request.user.post_set.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)



class PhotoList(generics.ListCreateAPIView):
    serializer_class = Photoserializer


    def get_queryset(self):
        print(self.request.user.pk)
        return self.request.user.photo_set.all()


