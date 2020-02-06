from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `advertiser` attribute.
    """

    message = "Not an owner of Demand or an Admin."

    def has_object_permission(self, request, view, obj):
        # Users of the group `admin` can have access.
        if request.user.groups.filter(name='admin').exists():
            return True
        else:
        # Instance must have an attribute named `advertiser`.
            return obj.advertiser == request.user
