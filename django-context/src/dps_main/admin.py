from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Contact, Cause, Promise
from .utilities.admin import register_admin_views

admin.site.register(User)
admin.site.register(Group)

admin.site.register(Contact)
admin.site.register(Cause)
admin.site.register(Promise)

register_admin_views()