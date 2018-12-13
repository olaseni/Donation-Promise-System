from random import randint

from django.core.management.base import BaseCommand, CommandError

from dps_main.utilities import faker


class Command(BaseCommand):
    help = 'Generates random sample data for the app'

    @staticmethod
    def _generate_data():
        """
        Create models
        """
        # create a bunch of causes
        faker.bulk_causes(320)

        # create a bunch of users
        faker.bulk_users(randint(40, 60))

        return faker.make_bulk_promises(300 * 35)

    def handle(self, *args, **options):
        try:
            e = self._generate_data()
            if isinstance(e, Exception):
                raise e
            self.stdout.write(self.style.SUCCESS('Success!'))
        except Exception as e:
            raise CommandError(e)
