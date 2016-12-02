from .models import Post
from .serializers import Postserializer
from rest_framework import generics


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = Postserializer



