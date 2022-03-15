from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        current_user = request.user

        if view.action in ['list', 'create', 'destroy', 'update', 'partial_update']:
            return (current_user.is_authenticated and current_user.is_superuser)
        elif view.action in ['retrieve']:
            return (current_user.is_authenticated and (
                current_user.is_superuser or current_user.is_staff or current_user.is_admin))
        else:
            return False
