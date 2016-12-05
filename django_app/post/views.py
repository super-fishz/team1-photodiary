from .models import Post
from .serializers import Postserializer
from rest_framework import generics
from member.models import MyUser


class PostList(generics.ListCreateAPIView):
    serializer_class = Postserializer

    def get_queryset(self):
        print(self.request.user.pk)
        return self.request.user.post_set.all()

