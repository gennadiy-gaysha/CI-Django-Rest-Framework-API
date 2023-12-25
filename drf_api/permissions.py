from rest_framework import permissions

# permissions.BasePermission: This class is provided by Django REST framework and
# serves as a base class for custom permission classes.
class IsOwnerOrReadOnly(permissions.BasePermission):
    # has_object_permission method is called by Django REST framework to
    # determine whether a user has permission to perform a certain action on
    # a specific object.
    # self: The instance of the IsOwnerOrReadOnly class.
    # request: The HTTP request object.
    # view: The view that is making the request.
    # obj: The object on which the permission check is being performed.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # For unsafe methods (POST, PUT, PATCH, DELETE), check if the user making
        # the request is the owner of the object.
        #  The permission is granted only if the user making the request
        #  (request.user) is the owner of the object (obj.owner).
        return obj.owner == request.user