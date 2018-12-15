from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError

from dps_main.models import Contact, Promise
from dps_main.tests import DpsTestCase
from dps_main.utilities.actions import ActionHelper


class PromiseActionsTestCase(DpsTestCase):

    @staticmethod
    def _create_cause(user, contact, cause_user):
        """
        Shorthand for creating causes
        """
        ah = ActionHelper(user)
        return ah.create_cause(title='Title', description='Description', contact=contact,
                               expiration_date=date.today(), target_amount=30000, creator=cause_user)

    @staticmethod
    def _list_available_causes(user):
        """
        Shorthand for reading causes
        """
        ah = ActionHelper(user)
        return ah.list_available_causes()

    @staticmethod
    def _make_promise(user, cause_id):
        """
        Shorthand for adding promises
        """
        ah = ActionHelper(user)
        return ah.add_promise_to_cause(cause_id, user=user, amount=30, target_date=date.today())

    @staticmethod
    def _list_promises(user):
        """
        Shorthand for reading promises
        """
        ah = ActionHelper(user)
        return ah.list_promises()

    @staticmethod
    def _read_promise(user, _id):
        """
        Shorthand for reading a promise
        """
        ah = ActionHelper(user)
        return ah.get_promise(_id)

    @staticmethod
    def _update_promise(user, _id, **kwargs):
        """
        Shorthand for updating a promise
        """
        ah = ActionHelper(user)
        return ah.update_promise(_id, **kwargs)

    @staticmethod
    def _delete_promise(user, _id):
        """
        Shorthand for deleting a promise
        """
        ah = ActionHelper(user)
        return ah.delete_promise(_id)

    def setUp(self):
        """
        Fixtures
        """
        cn = Contact.objects.create(id=1, first_name='First', last_name='Last', address='Address',
                                    phone='+00000000',
                                    email='a@email.com')
        cn2 = Contact.objects.create(id=2, first_name='First', last_name='Last', address='Address',
                                     phone='+00000000',
                                     email='a@email.com')
        cn3 = Contact.objects.create(id=3, first_name='First', last_name='Last', address='Address',
                                     phone='+00000000',
                                     email='a@email.com')
        cn4 = Contact.objects.create(id=4, first_name='First', last_name='Last', address='Address',
                                     phone='+00000000',
                                     email='a@email.com')
        self.user = User.objects.create_user('user', 'email@email.com', 'fasfj20r92f3')
        su = User.objects.create_superuser('admin5', 'super@email.com', 'sgsgsgsgwt2r2t23')
        # create a cause for a superuser
        cu = self._create_cause(su, cn, su)
        # save ref
        self.cu_id = cu.id
        self.su = su
        self.cn, self.cn2, self.cn3, self.cn4 = cn, cn2, cn3, cn4

    def test_make_promise(self):
        """
        GIVEN a normal member user
        WHEN attempting to create promises related to a cause
        THEN promise add operations should work as expected in the context of the user
        """

        p = self._make_promise(self.user, self.cu_id)
        self.assertIsInstance(p, Promise)

        # assert that user can make only one promise on cause
        with self.assertRaises(IntegrityError):
            self._make_promise(self.user, self.cu_id)

    def test_read_promises(self):
        """
        GIVEN a normal member user
        WHEN attempting to read/list promises related to a cause
        THEN read operations should work as expected in the context of the user
        """

        # normal user makes a promise
        p = self._make_promise(self.user, self.cu_id)
        # super user makes a promise
        p2 = self._make_promise(self.su, self.cu_id)

        # attempt to read own promise
        self.assertIsInstance(self._read_promise(self.user, p.id), Promise)
        # attempt to list promises should only expose own promises
        self.assertEqual(len(self._list_promises(self.user)), 1)

        # attempt to read other user's promise should fail
        with self.assertRaises(Promise.DoesNotExist):
            self.assertIsInstance(self._read_promise(self.user, p2.id), Promise)

        # super user should read same fine
        self.assertIsInstance(self._read_promise(self.su, p2.id), Promise)
        # super user should see all promises
        self.assertEqual(len(self._list_promises(self.su)), 2)

    def test_update_promises(self):
        """
        GIVEN a normal member user
        WHEN attempting to read/list promises related to a cause
        THEN read operations should work as expected in the context of the user
        """

        # normal user makes a promise
        p = self._make_promise(self.user, self.cu_id)
        # super user makes a promise
        p2 = self._make_promise(self.su, self.cu_id)

        # attempt to update own promise
        self._update_promise(self.user, p.id, amount=1029)
        self.assertEqual(self._read_promise(self.user, p.id).amount, 1029)

        # attempt to update other user
        with self.assertRaises(Promise.DoesNotExist):
            self._update_promise(self.user, p2.id, amount=1030)
            self.assertEqual(self._read_promise(self.user, p2.id).amount, 1030)

    def test_delete_promises(self):
        """
        GIVEN a normal member user
        WHEN attempting to delete promises related to a cause
        THEN delete operations should work as expected in the context of the user
        """

        # normal user makes a promise
        p = self._make_promise(self.user, self.cu_id)
        # super user makes a promise
        p2 = self._make_promise(self.su, self.cu_id)

        # attempt to delete own promise
        self._delete_promise(self.user, p.id)
        # should see no more promises
        self.assertEqual(len(self._list_promises(self.user)), 0)

        # attempt to delete other user's promise should fail, but not raise exception
        self._delete_promise(self.user, p2.id)
        # confirm by reading again
        self.assertIsInstance(self._read_promise(self.su, p2.id), Promise)

        # make again
        p = self._make_promise(self.user, self.cu_id)

        # super user should delete same and own fine
        self._delete_promise(self.su, p.id)
        self._delete_promise(self.su, p2.id)

        # no more promises here
        self.assertEqual(len(self._list_promises(self.su)), 0)

    def test_available_causes(self):
        """
        GIVEN a normal member user who has made a promise to a cause
        WHEN attempting to read/list promises related to a cause
        THEN read operations should work as expected in the context of availability
        """

        # user should see a total of 1 available cause(s)
        self.assertEqual(len(self._list_available_causes(self.user)), 1)

        # normal user makes a promise
        self._make_promise(self.user, self.cu_id)
        self.assertEqual(len(self._list_promises(self.user)), 1)

        # user should now see a total of 0 available cause(s)
        self.assertEqual(len(self._list_available_causes(self.user)), 0)

    def test_promises_for_cause(self):
        """
        GIVEN a cause
        WHEN attempting to list promises related to that cause
        THEN list operations should work as expected
        """
        ahs = ActionHelper(self.su)

        # no promises initially
        self.assertEqual(len(ahs.list_promises_by_cause(self.cu_id)), 0)

        # normal user makes a promise on that cause
        self._make_promise(self.user, self.cu_id)

        # 1 promise now
        self.assertEqual(len(ahs.list_promises_by_cause(self.cu_id)), 1)

        # super user makes a promise on that cause
        self._make_promise(self.su, self.cu_id)

        # 2 promises now
        self.assertEqual(len(ahs.list_promises_by_cause(self.cu_id)), 2)

    def test_promise_for_cause(self):
        """
        GIVEN a cause
        WHEN attempting to get user promise attached to that cause
        THEN read operations should work as expected
        """
        ah = ActionHelper(self.user)

        # normal user makes a promise on that cause
        self._make_promise(self.user, self.cu_id)

        # retrieves promise
        p = ah.get_promise_for_cause(self.cu_id).get()
        self.assertIsInstance(p, Promise)

        # other user makes a promise on that cause
        self._make_promise(self.su, self.cu_id)

        # retrieves same promise again
        self.assertEqual(ah.get_promise_for_cause(self.cu_id).get().id, p.id)

    def test_all_causes_promised(self):
        """
        GIVEN some causes
        WHEN selectively make promises to those causes
        THEN this operation should reflect the number of causes promised
        """

        # create a couple more causes
        c1 = self._create_cause(self.su, self.cn2, self.su)
        self._create_cause(self.su, self.cn3, self.su)
        c3 = self._create_cause(self.su, self.cn4, self.su)

        ah = ActionHelper(self.su)

        # should list 4 causes
        self.assertEqual(len(ah.list_causes()), 4)

        # promise on 2
        self._make_promise(self.user, c1.id)
        self._make_promise(self.user, c3.id)

        # should list 2
        self.assertEqual(len(ah.list_all_causes_promised()), 2)
