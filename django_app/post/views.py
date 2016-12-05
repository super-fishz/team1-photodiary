from django.http import HttpResponse
from rest_framework import generics
from .models import Photo, Post
from .serializers import Photoserializer, Postserializer
from member.models import MyUser
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView):
    serializer_class = Postserializer

    def get_queryset(self):
        # print(Photo.objects.get(po지금 현재 불러오려고 하는 포스트의 pkst=))
        return self.request.user.post_set.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        for file in request.FILES.getlist('image'):
            Photo.objects.create(
                post=post,
                image=file
            )
        return Response(serializer.data)



class PhotoList(generics.ListCreateAPIView):
    serializer_class = Photoserializer
    queryset = {'post', 'image'}

    # def get_queryset(self):
    #     print(self.request.user.pk)
    #     return self.request.user.photo_set.all()


