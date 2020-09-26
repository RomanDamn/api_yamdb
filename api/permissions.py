from rest_framework import permissions
from rest_framework.permissions import BasePermission


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or permissions.IsAdminUser)