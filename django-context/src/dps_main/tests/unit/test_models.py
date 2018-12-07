from django.test import TestCase
from dps_main.models import Contact


# Create your tests here.

class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(first_name="Barrack", last_name="Obama", address="White House",
                               phone="+111111111", email="potus@whitehouse.gov")

    def test_contacts(self):
        """*"""
        self.assertEqual(Contact.objects.count(), 1)
