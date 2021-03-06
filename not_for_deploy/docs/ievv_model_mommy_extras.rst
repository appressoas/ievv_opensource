###############################################################################
`ievv_model_mommy_extras` --- Add support for more fields types to model-bakery
###############################################################################

Model-bakery does not support all the fields in Django. To remidy this,
we provide the ``ievv_opensource.ievv_model_mommy_extras``.

It is named ievv_model_mommy_extras for historical reasons - model_mommy was renamed to model_bakery at some point.

For now it only adds support for::

- django.contrib.postgres.fields.ranges.DateTimeRangeField
- django.contrib.postgres.fields.ranges.DateRangeField


*****
Setup
*****
To use this, you only need to add it to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # Other apps ...
        'ievv_opensource.ievv_model_mommy_extras'
    ]

.. note:: You only need this for testing, so if you have split out your test settings,
    you should only add it to ``INSTALLED_APPS`` there.
