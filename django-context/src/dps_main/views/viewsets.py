from django.urls import reverse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from dps_main.permissions.rest_framework import IsAdminSuper, IsAuthenticatedOwnerOrSuperForPromises, \
    IsAuthenticatedAdmin
from dps_main.serializers import ContactSerializer, CauseSerializer, PromiseSerializer
from dps_main.models import Contact, Cause, Promise
from dps_main.utilities.actions import ActionHelper
from dps_main.utilities.reports import top_causes_by_amount, top_causes_by_promises


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

    @property
    def action_permissions(self):
        try:
            if not hasattr(self, '_action_permissions'):
                setattr(self, '_action_permissions',
                        getattr(getattr(self, self.action, None), 'kwargs', {}).get('permission_classes', []))
            return getattr(self, '_action_permissions', [])
        except (AttributeError, KeyError):
            return []


class ModelViewSet(UsefulComponentsMixins, viewsets.ModelViewSet):
    """
    Replace permissions with the ones on actions if present.
    DRF doesn't do that originally
    """

    # add up action permissions instead of replacing them
    action_permissions_are_inclusive = False

    def get_permissions(self):
        if self.action_permissions_are_inclusive:
            self.permission_classes = list(set((self.permission_classes or []) + self.action_permissions))
        else:
            self.permission_classes = self.action_permissions or self.permission_classes
        return super().get_permissions()


class ContactViewSet(viewsets.ModelViewSet):
    """
    Views for `Contacts`
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CauseViewSet(ModelViewSet):
    """
    Views for `Cause`
    """
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    action_permissions_are_inclusive = True

    def get_permissions(self):
        """
        Model permissions kick in for safe methods, which mostly means readonly access for anon users.
        On the flip side you need to be an admin to modify
        """
        if not self.safe_request_method:
            self.permission_classes = [IsAdminSuper]
        return super().get_permissions()

    def get_serializer_class(self):
        if any([self.action == item for item in ('promise', 'promises',)]):
            return PromiseSerializer
        return super().get_serializer_class()

    def _respond_with_instances(self, causes, detail=False):
        """
        Returns instances to DRF
        """

        if not detail:
            page = self.paginate_queryset(causes)
            if page is not None:
                serializer = self.get_serializer(page, many=not detail)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(causes, many=not detail)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Available causes are causes not yet promised by user
        """
        return self._respond_with_instances(self.action_helper.list_available_causes())

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedAdmin])
    def promises(self, request, pk=None):
        """
        admin only, returns all promises for a cause
        """
        return self._respond_with_instances(self.action_helper.list_promises_by_cause(pk))

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def promise(self, request, pk=None):
        """
        returns a promise associated with a cause for a user
        """
        return self._respond_with_instances(self.action_helper.get_promise_for_cause(pk).get(), detail=True)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def promised(self, request):
        """
        all causes which user has promised
        """
        return self._respond_with_instances(self.action_helper.list_all_causes_promised())

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedAdmin], url_path='top/amount')
    def top_amount(self, request):
        """
        all causes which user has promised
        """
        return self._respond_with_instances(top_causes_by_amount())

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedAdmin], url_path='top/promised')
    def top_promised(self, request):
        """
        all causes which user has promised
        """
        return self._respond_with_instances(top_causes_by_promises())


class PromiseViewSet(ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = [IsAuthenticatedOwnerOrSuperForPromises]

    def update(self, request, *args, **kwargs):
        """
        provide/override cause and user, as we don't want these to change
        """
        if any(index in request.data for index in ('cause', 'user')):
            raise AssertionError('You cannot change `user` or `cause`')
        request.data.update(dict(cause=Promise.objects.values_list('cause_id', flat=True).get(pk=kwargs.get('pk')),
                                 user=request.user.id))
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def make(self, request, pk=None):
        """
        Make a promise to a cause
        """
        if not request.user.is_authenticated:
            self.permission_denied(request, 'Not allowed!')

        data = request.data.copy()
        data.update(dict(cause=pk, user=request.user.id))
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
