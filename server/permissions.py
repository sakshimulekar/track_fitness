from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user
    

class IsOwnerOrReadOnlyTrainer(permissions.BasePermission):
    """
    Custom permission to only allow owners of a trainer profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the trainer profile.
        return obj.trainer == request.user
    

class IsOwnerOrReadOnlyPlan(permissions.BasePermission):
    """
    Custom permission to allow owners of a workout plan to edit it,
    but only allow read access to others.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Edit permissions are only allowed to the owner of the workout plan.
        return obj.trainer == request.user