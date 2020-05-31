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
    Custom permissions to only allow volunteers of a location to edit/create a status
    """

    def has_object_permission(self, request, view, obj):
        """
        Assert if user has permission. Obj may be a location or a status (eg : while closing a status)
        """
        try:    # Trying to see if object is a Status instance or a Location instance.
            obj = obj.location
        except AttributeError:
            pass
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user in obj.volunteers.filter(is_active=True):
            return True
        elif request.user == obj.moderator:
            return True