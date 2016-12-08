import json

from django.core import serializers
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView

from .models import Photo, Post
from .serializers import PhotoSerializer, PostSerializer
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.request.user.post_set.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        for file in request.FILES.getlist('image'):
            Photo.objects.create(post=post, image=file)
        return Response(serializer.data)


class PostDetail(APIView):

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        origin_serializer = PostSerializer(post)
        origin_title = origin_serializer.data['title']
        modify_serializer = PostSerializer(post, data=request.data)
        if modify_serializer.is_valid():
            modify_serializer.save()
            return Response(modify_serializer.data)
        elif 'title' not in request.data:
            request.data['title'] = origin_title
            modify_serializer = PostSerializer(post, data=request.data)
            if modify_serializer.is_valid():
                modify_serializer.save()
                return Response(modify_serializer.data)
        else:
            return Response(modify_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoDetail(APIView):

    def get_post_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, format=None):
        post = self.get_post_object(post_pk)
        post_serializer = PostSerializer(post)
        post_photo_list = post_serializer.data['photos']
        return Response(post_photo_list)

    def put(self, request, post_pk, format=None):
        photo = self.get_post_object(post_pk)
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, format=None):
        post = self.get_post_object(post_pk)
        photos = post.photo_set.all()
        photos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

