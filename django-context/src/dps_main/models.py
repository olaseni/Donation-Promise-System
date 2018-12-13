from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta


def tomorrow():
    return now() + timedelta(days=1)


class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F'Contact <{self.id}, {self.first_name} {self.last_name}>'

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ['-created']


class Cause(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(help_text="Full description of the cause. This will be displayed to the user")
    illustration = models.ImageField(help_text='Images associated with the cause',
                                     upload_to='illustration/%Y/%m/%d/')
    contact = models.OneToOneField(Contact, verbose_name='Primary Contact',
                                   help_text="Contact associated with the cause",
                                   on_delete=models.CASCADE)
    expiration_date = models.DateField(help_text="Date for which this cause is no longer valid",
                                       default=tomorrow)
    target_amount = models.FloatField('Amount targeted, NGN', default=0.0, help_text="Amount targeted in NGN")
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return F'Cause <{self.id}, {self.title}>'

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ['-created']


class Promise(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField('Amount promised, NGN', help_text="Amount promised toward the associated cause, NGN")
    target_date = models.DateField(help_text="The date for which the promise is expected to be redeemed",
                                   default=tomorrow)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F'Promise <{self.id}, NGN {self.amount} for cause: ( {self.cause.title} )>'

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ['-created']
        unique_together = ('cause', 'user')
