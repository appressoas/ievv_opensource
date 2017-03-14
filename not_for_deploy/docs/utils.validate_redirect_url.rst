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


****************
Typical use case
****************
Lets say you have a login view that supports ``?next=<some url or path>``. This
could lead to attacks for mining personal information if someone shares a link
where the next URL points to an external domain. What you want is probably to allow
redirects within your domain. To achieve this, you only need to set the
:setting:`IEVV_VALID_REDIRECT_URL_REGEX` setting to match your domain and paths without
a domain, and do something like this in your login view::

    from ievv_opensource.utils import validate_redirect_url

    class MyLoginView(...):
        # ... other code ...

        def get_success_url(self):
            nexturl = self.request.GET.get('next')
            if nexturl:
                validate_redirect_url.validate_url(nexturl)
                return nexturl
            else:
                # return some default

This will raise a ValidationError if the validation fails. You may cach this
exception if you want to handle this with something other than a crash message
in your server log.


*********
Functions
*********

.. currentmodule:: ievv_opensource.utils.validate_redirect_url
.. automodule:: ievv_opensource.utils.validate_redirect_url
