from dps_main.models import Contact
from dps_main.tests import DpsTestCase


class ContactTestCase(DpsTestCase):
    def setUp(self):
        self.assertTestEnvironment()
        Contact.objects.create(first_name="Barrack", last_name="Obama", address="White House",
                               phone="+111111111", email="potus@whitehouse.gov")

    def test_contacts(self):
        """*"""
        self.assertEqual(Contact.objects.count(), 1)
