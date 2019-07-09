from rest_framework import permissions


class IsOwnerTask(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.consumer == request.user


class IsConsumerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'consumer'
