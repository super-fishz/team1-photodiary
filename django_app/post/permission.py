from rest_framework import permissions
from .models import Post


class Isthatyours(permissions.BasePermission):
    message = '요청하신것은 본인것이 아닙니다. ㅠㅠ'

    def has_permission(self, request, view):
        return request.user == Post.objects.get(pk=view.kwargs['post_pk']).author
