from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class OwnResourcePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS and
                request.user.is_anonymous or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return (obj.author == request.user or
                    request.user.role == 'admin' or
                    request.user.role == 'moderator')
        return True
