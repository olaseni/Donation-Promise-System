from rest_framework.permissions import DjangoModelPermissions, BasePermission, IsAdminUser


class SafeDjangoModelPermissions(DjangoModelPermissions):
    """
    Overrides the `DjangoModelPermissions` by restricting GET etc methods
    """

    @property
    def perms_map(self):
        """
        Combines the permissions map from the superclass with new ones that support SAFE METHODS
        """
        return {**super().perms_map, **{
            'GET': ['%(app_label)s.view_%(model_name)s'],
            'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
            'HEAD': ['%(app_label)s.view_%(model_name)s'],
        }}


class IsAdminSuper(BasePermission):
    """
    Allows access only to admin super users.
    """

    message = "You must be an admin/super"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser


class IsAuthenticatedOwnerOrSuperForPromises(BasePermission):
    """
    Allows access only to authenticated owners.
    """

    message = "You must be authenticated or a super"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, promise):
        owner_or_super = request.user == promise.user or request.user.is_superuser
        return request.user and request.user.is_authenticated and owner_or_super


class IsAuthenticatedAdmin(IsAdminUser):
    message = "You must be an authenticated admin"

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_authenticated

