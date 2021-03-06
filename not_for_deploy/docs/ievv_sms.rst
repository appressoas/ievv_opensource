########################################################
`ievv_sms` --- SMS sending - multiple backends supported
########################################################


************
Requirements
************
::

    $ pip install gsm0338


*****
Setup
*****
Add it to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # Other apps ...
        'ievv_opensource.ievv_sms'
    ]

For development, you probably also want to use the
:class:`ievv_opensource.ievv_sms.backends.debugprint.Backend` backend. You
configure that with the following setting::

    IEVV_SMS_DEFAULT_BACKEND_ID = 'debugprint'


***********
Sending SMS
***********
Send an SMS using the default backend with::

    from ievv_opensource.ievv_sms.sms_registry import send_sms
    send_sms(phone_number='12345678', message='This is a test')

Send using another backend using the ``backend_id`` argument::

    from ievv_opensource.ievv_sms.sms_registry import send_sms
    send_sms(phone_number='12345678', message='This is a test',
             backend_id='some_backend_id')

See :func:`ievv_opensource.ievv_sms.sms_registry.send_sms` for more details.


*************************
Creating a custom backend
*************************
See the example in :class:`~ievv_opensource.ievv_sms.sms_registry.AbstractSmsBackend`.



******************************
Specifying the default backend
******************************
Just set the backend ID (see :meth:`~ievv_opensource.ievv_sms.sms_registry.AbstractSmsBackend.get_backend_id`)
of a backend in the :setting:`IEVV_SMS_DEFAULT_BACKEND_ID` setting.



********
Core API
********

send_sms()
==========

.. currentmodule:: ievv_opensource.ievv_sms.sms_registry
.. autofunction:: ievv_opensource.ievv_sms.sms_registry.send_sms


AbstractSmsBackend
==================

.. currentmodule:: ievv_opensource.ievv_sms.sms_registry
.. autoclass:: ievv_opensource.ievv_sms.sms_registry.AbstractSmsBackend


Registry
========

.. currentmodule:: ievv_opensource.ievv_sms.sms_registry
.. autoclass:: ievv_opensource.ievv_sms.sms_registry.Registry


********
Backends
********

Debug/develop backends
======================
.. currentmodule:: ievv_opensource.ievv_sms.backends.debugprint
.. automodule:: ievv_opensource.ievv_sms.backends.debugprint


PSWIN backend
=============
.. currentmodule:: ievv_opensource.ievv_sms.backends.pswin
.. automodule:: ievv_opensource.ievv_sms.backends.pswin

DebugSmsMessage backend
=============
.. currentmodule:: ievv_opensource.ievv_sms.backends.debug_dbstore
.. automodule:: ievv_opensource.ievv_sms.backends.debug_dbstore
