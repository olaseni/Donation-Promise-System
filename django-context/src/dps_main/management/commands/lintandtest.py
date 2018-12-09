from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from subprocess import check_call, CalledProcessError


class Command(BaseCommand):
    help = 'Runs the linter and test suites'

    def handle(self, *args, **options):
        try:
            check_call(['flake8', '.'])
            call_command('test')
            self.stdout.write(self.style.SUCCESS('Success!'))
        except CalledProcessError as e:
            raise CommandError(e.output or e)
