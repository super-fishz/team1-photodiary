from rest_framework.serializers import ModelSerializer
from .models import Post


class Postserializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'content', 'modified_date', 'created_date')
