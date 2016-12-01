from rest_framework.serializers import ModelSerializer
from .models import Photo


class Photoserializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'author', 'content', 'modified_date', 'created_date', 'image', 'post')
