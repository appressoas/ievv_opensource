from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set the passwords of all users to "test". Very useful ' \
           'when loading a production dump locally for testing/debugging.'

    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        user_model.objects.all().update(password=make_password('test'))
