from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or permissions.IsAdminUser)


class IsAdminPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
