##########################################
`utils.ievv_json` --- Json encoder/decoder
##########################################

Usage
=====

You use the module just like the python json module for all simple use-cases::

    from ievv_opensource.utils import ievv_json
    import datetime
    import decimal
    import arrow
    from django.contrib.auth import get_user_model

    json_data = ievv_json.dumps({
        'name': 'Test',
        'score_weight': decimal.Decimal('2.333342'),
        'created_datetime': arrow.get(datetime.datetime(2012, 12, 24, 12, 33), 'Europe/Oslo').datetime,
        'last_changed_by': get_user_model().objects.get(email='someone@example.com')
    })
    print(json_data)

    decoded_back_to_dict = ievv_json.loads(json_data)
    print(decoded_back_to_dict)


See :class:`ievv_opensource.utils.ievv_json.Encoder` for overview over the extra
types we support.


Classes and functions
=====================

.. currentmodule:: ievv_opensource.utils.ievv_json
.. automodule:: ievv_opensource.utils.ievv_json
