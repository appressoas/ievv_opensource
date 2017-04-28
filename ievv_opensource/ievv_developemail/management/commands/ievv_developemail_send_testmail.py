# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run ievv_customsql.'

    def add_arguments(self, parser):
        parser.add_argument('--html', dest='html',
                            required=False, action='store_true',
                            help='Send html email.')
        parser.add_argument('--use-cradmin-email', dest='use_cradmin_email',
                            required=False, action='store_true',
                            help='Use django_cradmin.apps.cradmin_email.emailutils.AbstractEmail '
                                 'instead of just the send_mail() function.')

    def __get_plaintext_message(self):
        return 'Maecenas faucibus mollis interdum. Cum sociis ' \
               'natoque penatibus et magnis dis parturient montes, ' \
               'nascetur ridiculus mus. Praesent commodo cursus magna, ' \
               'vel scelerisque nisl consectetur et. Fusce dapibus, ' \
               'tellus ac cursus commodo, tortor mauris condimentum ' \
               'nibh, ut fermentum massa justo sit amet risus. Etiam ' \
               'porta sem malesuada magna mollis euismod. Cras mattis ' \
               'consectetur purus sit amet fermentum. Donec ullamcorper ' \
               'nulla non metus auctor fringilla.' \
               '\n\n' \
               'Duis mollis, est non commodo luctus, nisi erat porttitor ' \
               'ligula, eget lacinia odio sem nec elit. Maecenas sed diam ' \
               'eget risus varius blandit sit amet non magna. Vivamus ' \
               'sagittis lacus vel augue laoreet rutrum faucibus dolor ' \
               'auctor. Maecenas sed diam eget risus varius blandit sit ' \
               'amet non magna. Curabitur blandit tempus porttitor. ' \
               'Etiam porta sem malesuada magna mollis euismod. Vestibulum ' \
               'id ligula porta felis euismod semper.'

    def __get_html_message(self):
        return 'Maecenas <strong>faucibus</strong> mollis interdum. Cum sociis ' \
               'natoque penatibus et magnis dis parturient montes, ' \
               'nascetur ridiculus mus. Praesent commodo cursus magna, ' \
               'vel scelerisque nisl consectetur et. Fusce dapibus, ' \
               'tellus ac cursus commodo, tortor mauris condimentum ' \
               'nibh, ut fermentum massa justo sit amet risus. Etiam ' \
               'porta sem malesuada magna mollis euismod. Cras mattis ' \
               'consectetur purus sit amet fermentum. Donec ullamcorper ' \
               'nulla non metus auctor fringilla.' \
               '<br><br>' \
               '<em>Duis mollis</em>, est non commodo luctus, nisi erat porttitor ' \
               'ligula, eget lacinia odio sem nec elit. Maecenas sed diam ' \
               'eget risus varius blandit sit amet non magna. Vivamus ' \
               'sagittis lacus vel augue laoreet rutrum faucibus dolor ' \
               'auctor. <a href="http://example.com">Maecenas sed</a> ' \
               'diam eget risus varius blandit sit ' \
               'amet non magna. Curabitur blandit tempus porttitor. ' \
               'Etiam porta sem malesuada magna mollis euismod. Vestibulum ' \
               'id ligula porta felis euismod semper.'

    def __get_email_kwargs(self, html):
        kwargs = {
            'subject': 'Test email',
            'message': self.__get_plaintext_message(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': ['testrecipient@example.com']
        }
        if html:
            kwargs['html_message'] = self.__get_html_message()
        return kwargs

    def handle(self, *args, **options):
        html = options['html']
        send_mail(**self.__get_email_kwargs(html=html))
