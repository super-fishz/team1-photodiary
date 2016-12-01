from .models import Photo
from .serializers import Photoserializer
from rest_framework import generics


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = Photoserializer