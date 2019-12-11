from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.moderator == request.user

class IsVolunteerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions ton only allow volunteers of an object to add a status
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in obj.location.volunteers.all()
