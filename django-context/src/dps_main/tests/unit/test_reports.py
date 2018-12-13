from random import randint, choice, sample

from django.contrib.auth.models import User

from dps_main.models import Cause, Promise
from dps_main.tests import DpsTestCase

from dps_main.utilities import faker

from dps_main.utilities.reports import top_causes_by_amount, top_causes_by_promises


def _create_fixtures():
    """
    Create models
    """
    # create a bunch of causes
    creator = faker.bulk_causes(201)
    causes = Cause.objects.all()

    # causes size
    causes_size = len(causes)
    causes_half = causes_size // 2
    # create a bunch of users
    faker.bulk_users(randint(52, 95))
    users = User.objects.all()
    # users size
    users_size = len(users)

    # categorize causes
    first_causes, last_causes = causes[:causes_half], causes[causes_half:]

    # select cause to promise the most money
    money_cause = choice(first_causes)
    # select cause to give the most promises
    number_cause = choice(last_causes)

    # make a bunch of promises

    # a high enough amount to guarantee top placement
    promise_list = [faker.make_promise(user=creator, cause=money_cause, amount=99999999)[0]]
    for cause in sample(first_causes, causes_half - 2):
        user = choice(users)
        amount = 99999999 if cause is money_cause else None
        promise_list.append(faker.make_promise(user=user, cause=cause, amount=amount)[0])

    for i in range(users_size - 5 if users_size > 5 else users_size):
        user = users[i]
        promise_list.append(faker.make_promise(user=user, cause=number_cause)[0])

    faker.make_bulk_promises_with_data_list(promise_list)

    return money_cause, number_cause


class ReportsTestCase(DpsTestCase):

    def setUp(self):
        self.assertTestEnvironment()
        self.money_cause, self.number_cause = _create_fixtures()

    def test_causes_and_promises_created(self):
        """
        GIVEN fixtures were run
        WHEN causes and promises were inserted into the db
        THEN objects must exist
        """
        self.assertGreater(Cause.objects.count(), 0)
        self.assertGreater(Promise.objects.count(), 0)

    def test_top_cause_by_amount(self):
        """
        GIVEN reports are run
        WHEN asked for the top grossing causes in amount promised
        THEN the highest amount must be at the head
        """
        q = top_causes_by_amount()
        self.assertEqual(q[0].id, self.money_cause.id)

    def test_top_cause_by_number(self):
        """
        GIVEN reports are run
        WHEN asked for the top grossing causes in promises made
        THEN the highest amount must be at the head
        """
        q = top_causes_by_promises()
        self.assertEqual(q[0].id, self.number_cause.id)
