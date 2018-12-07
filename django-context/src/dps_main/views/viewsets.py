from django.contrib.auth.models import User
from rest_framework import viewsets
from dps_main.serializers import UserSerializer, ContactSerializer, CauseSerializer, PromiseSerializer
from dps_main.models import Contact, Cause, Promise


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CauseViewSet(viewsets.ModelViewSet):
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
