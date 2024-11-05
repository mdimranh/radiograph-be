from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request):
        user = request.user
        if user.is_authenticated:
            return user.role.name == "admin"
