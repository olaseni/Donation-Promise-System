from rest_framework.permissions import DjangoModelPermissions


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
