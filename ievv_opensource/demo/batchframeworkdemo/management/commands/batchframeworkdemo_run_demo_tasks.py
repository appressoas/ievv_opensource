from django.core.management.base import BaseCommand, CommandError

from ievv_opensource.ievv_batchframework import batchregistry


class Command(BaseCommand):
    help = 'Run batchframeworkdemo.'

    def handle(self, *args, **options):
        result = batchregistry.Registry.get_instance().run(
            actiongroup_name='batchframeworkdemo_helloworld',
            test='hello')
        print(result)
