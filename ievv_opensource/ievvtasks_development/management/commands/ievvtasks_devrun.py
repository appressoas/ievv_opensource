from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run development servers configured for this project.'

    # def add_arguments(self, parser):
    #     parser.add_argument('-w', '--watch', dest='watch',
    #                         required=False, action='store_true',
    #                         help='Starts a blocking process that watches for changes.')

    def handle(self, *args, **options):
        settings.IEVVTASKS_DEVELOPRUN_THREADLIST.start()
