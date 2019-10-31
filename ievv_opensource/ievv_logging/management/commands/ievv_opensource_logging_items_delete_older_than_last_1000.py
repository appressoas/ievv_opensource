import sys
from django.core.management.base import BaseCommand


from ievv_opensource.ievv_logging.models import IevvLoggingEventBase


def delete_older_than_the_last_100():
    for loggingeventbase in IevvLoggingEventBase.objects.all():
        last_created_item_ids = loggingeventbase.ievvloggingeventitem_set.all()[:100].values_list('id', flat=True)
        items = loggingeventbase.ievvloggingeventitem_set.exclude(pk__in=list(last_created_item_ids))
        sys.stdout.write(f'Deleting {items.count()} for {loggingeventbase.slug}\n')
        items.delete()


class Command(BaseCommand):
    help = 'Deletes IevvLoggingEventItem rows for each IevvLoggingEventBase except the last 100.'

    def handle(self, *args, **options):
        delete_older_than_the_last_100()
