from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from dps_main.permissions.rest_framework import IsAdminSuperUser
from dps_main.serializers import ContactSerializer, CauseSerializer, PromiseSerializer
from dps_main.models import Contact, Cause, Promise
from dps_main.utilities.actions import ActionHelper


class UsefulComponentsMixins(object):
    """
    Mixin requires instances with attributes:
    - request (imbued intrinsically in all views, :))
    """

    @property
    def safe_request_method(self) -> bool:
        return self.request.method in permissions.SAFE_METHODS

    @property
    def action_helper(self) -> ActionHelper:
        """
        Imbued in app's own middleware
        :return: ActionHelper
        """
        return self.request.action_helper


class ContactViewSet(viewsets.ModelViewSet):
    """
    Views for `Contacts`
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CauseViewSet(UsefulComponentsMixins, viewsets.ModelViewSet):
    """
    Views for `Cause`
    """
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer

    def get_permissions(self):
        """
        Model permissions kick in for safe methods, which mostly meads readonly access for anon users.
        On the flip side you need to be an admin to modify
        """
        self.permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
        if not self.safe_request_method:
            self.permission_classes = [IsAdminSuperUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Available causes are causes not yet promised by user
        """
        causes = self.action_helper.list_available_causes()

        page = self.paginate_queryset(causes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(causes, many=True)
        return Response(serializer.data)


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
