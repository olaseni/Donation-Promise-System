from django.urls import reverse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from dps_main.permissions.rest_framework import IsAdminSuper
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
        Model permissions kick in for safe methods, which mostly means readonly access for anon users.
        On the flip side you need to be an admin to modify
        """
        self.permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
        if not self.safe_request_method:
            self.permission_classes = [IsAdminSuper]
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


class PromiseViewSet(UsefulComponentsMixins, viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def make(self, request, pk=None):
        """
        Make a promise to a cause
        """

        if not request.user.is_authenticated:
            self.permission_denied(request, 'Not allowed!')

        self.check_permissions(request)

        data = request.data.copy()
        data['cause'] = pk
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        promise_data = data.copy()
        promise_data.pop('cause')
        promise = self.action_helper.add_promise_to_cause(pk, **promise_data)

        if not promise:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data[api_settings.URL_FIELD_NAME] = reverse('promise-detail', args=[promise.id])
        headers = self.get_success_headers(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
