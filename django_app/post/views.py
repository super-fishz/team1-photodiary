from rest_framework import generics
from .models import Photo
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


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = {'post', 'image'}


