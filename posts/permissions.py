import re

from rest_framework.permissions import BasePermission

from .models import Post


class OwnPostOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']: return True
        pattern = '\d+'
        match = re.search(pattern, request.path)
        if match is None: return True
        post_id = request.path[match.start():match.end()]
        post = Post.objects.filter(id=post_id)
        return not post.exists() or post.first().owner == request.user