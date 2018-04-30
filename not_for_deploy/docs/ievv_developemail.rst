#####################################################################################
`ievv_developemail` --- Develop mail backend that lets you view mails in django admin
#####################################################################################


*****
Setup
*****

Add it to ``INSTALLED_APPS`` setting, and set the ``EMAIL_BACKEND`` setting (typically only in develop settings)::

    INSTALLED_APPS = [
        # ...
        'ievv_opensource.ievv_developemail',
    ]

    EMAIL_BACKEND = 'ievv_opensource.ievv_developemail.email_backend.DevelopEmailBackend'


Migrate::

    $ python manage.py migrate


You should now get new emails both logged to the terminal, and added as a DevelopEmail
object in the database which you can browse in Django admin.


************
How it works
************
We have a custom email backend that sends emails to the DevelopEmail database model
(and to log).


*****************************************
Management script for sending test emails
*****************************************
We provide the ``ievv_developemail_send_testmail`` management script for sending
test emails. It can be useful just to check that emails are sent, but also
for testing ``cradmin_email`` styling etc.

In its simplest form:

    $ python manage.py ievv_developemail_send_testmail --to "test@example.com"

The same, but with an HTML message::

    $ python manage.py ievv_developemail_send_testmail --to "test@example.com" --html

With a custom message instead of the default lorem ipsum message::

    $ python manage.py ievv_developemail_send_testmail --to "test@example.com" --html --message-html "Dette er <em>en test lizzm</em>"

Send using django_cradmin.apps.cradmin_email.emailutils.AbstractEmail::

    $ python manage.py ievv_developemail_send_testmail --to "test@example.com" --html --use-cradmin-email
    .. or with custom message ..
    $ python manage.py ievv_developemail_send_testmail --to "test@example.com" --html  --use-cradmin-email --message-html "Dette er <em>en test lizzm</em>"

From email can be set too! Defaults to the DEFAULT_FROM_EMAIL setting::

    $ python manage.py ievv_developemail_send_testmail --to "test@example.com" --from "from@example.com"
