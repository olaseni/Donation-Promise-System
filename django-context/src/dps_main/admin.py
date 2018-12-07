from django.contrib import admin
from .models import Contact, Cause, Promise

# Register your models here.
admin.site.register(Contact)
admin.site.register(Cause)
admin.site.register(Promise)
