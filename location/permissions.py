from rest_framework import permissions


class LocationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        current_user = request.user

        if view.action in ['create', 'destroy', 'update', 'partial_update']:
            return (current_user.is_authenticated and (
                current_user.is_superuser or current_user.is_staff or current_user.is_admin))
        else:
            return True