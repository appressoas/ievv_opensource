########################################################
`utils.validate_redirect_url` --- Validate redirect urls
########################################################

A very small set of utilities for validating a redirect URL.
You will typically use this to secure URLs that you get as input
from an insecure source, such as a ``?next=<anything>`` argument
for a login view.


*********
Configure
*********
The only configuration is via the :setting:`IEVV_VALID_REDIRECT_URL_REGEX`, where
you configure the valid redirect URLs.


*********
Functions
*********

.. currentmodule:: ievv_opensource.utils.validate_redirect_url
.. automodule:: ievv_opensource.utils.validate_redirect_url
