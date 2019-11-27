from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.moderator == request.user
