from rest_framework import serializers

from dps_main.models import Contact, Cause, Promise


#

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    # noinspection PyMethodMayBeStatic
    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


# Serializers define the API representation.

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'address', 'phone')


class CauseSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    illustration = Base64ImageField(max_length=None, use_url=True, )

    def create(self, validated_data):
        """
        Update user and nested contact
        """
        request = self._context['request']
        validated_data.update(dict(creator=request.user, creator_id=request.user.id))
        if request.data and 'contact' in request.data:
            contact = Contact.objects.create(**request.data['contact'])
            validated_data.update(dict(contact=contact, contact_id=contact.id))
        return super().create(validated_data)

    class Meta:
        model = Cause
        fields = ('id', 'title', 'description', 'illustration', 'contact', 'expiration_date',
                  'target_amount', 'enabled', 'created', 'modified')


class PromiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = ('amount', 'target_date', 'cause', 'user', 'created', 'modified')
