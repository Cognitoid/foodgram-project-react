from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorAdminModeratorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin()
                or request.user.is_moderator()
            )
        return request.method in SAFE_METHODS
