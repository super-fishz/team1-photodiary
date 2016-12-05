from rest_framework import generics
from .models import Photo
from .serializers import Photoserializer, Postserializer


class PostList(generics.ListCreateAPIView):
    serializer_class = Postserializer

    def get_queryset(self):
        print(self.request.user.pk)
        return self.request.user.post_set.all()




class PhotoList(generics.ListCreateAPIView):
    serializer_class = Photoserializer


    def get_queryset(self):
        print(self.request.user.pk)
        return self.request.user.post_set.all()


