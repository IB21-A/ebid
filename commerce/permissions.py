from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.

        if hasattr(obj, 'owner'):
            return (obj.owner == request.user)

        if hasattr(obj, 'creator'):
            return (obj.creator == request.user)

        if hasattr(obj, 'author'):
            return (obj.author == request.user)

        if hasattr(obj, 'user_id'):
            print('Permission:', obj.user_id == request.user)
            return (obj.user_id == request.user)


class IsOwner(permissions.BasePermission):
    # TODO add Admin access check. Currently only returns user.
    """
    Custom permission to only allow owners to read it
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Read/Write permissions are only allowed to the owner of the object.

        if hasattr(obj, 'user_id'):
            return (obj.user_id == request.user)

        if hasattr(obj, 'owner'):
            return (obj.owner == request.user)

        if hasattr(obj, 'creator'):
            return (obj.creator == request.user)

        if hasattr(obj, 'author'):
            return (obj.author == request.user)
