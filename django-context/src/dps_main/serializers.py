from rest_framework import serializers

from django.contrib.auth.models import User
from dps_main.models import Contact, Cause, Promise


# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'address', 'phone')


class CauseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cause
        fields = ('id', 'title', 'description', 'illustration', 'contact', 'expiration_date',
                  'target_amount', 'enabled', 'created', 'modified')


class PromiseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promise
        fields = ('amount', 'target_date', 'cause', 'user', 'created', 'modified')
