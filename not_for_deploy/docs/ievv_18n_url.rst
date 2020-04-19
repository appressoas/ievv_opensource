#######################################################################
`ievv_i18n_url` --- i18n support for various ways of routing i18n views
#######################################################################

Hosting a page in different languages can only be achived in a finite number of ways. These are the most common:

- The default django way where the selected language is stored in session.
- Some prefix to the URL path like ``/<languagecode>/path/to/my/view``,
  ``/l/<languagecode>/path/to/my/view``, etc. typically with the
  default translation at ``/path/to/my/view``
- Based on domain name. E.g. `myapp.com` for english, `myapp.no` for norwegian, etc., or `<languagecode>.myapp.com`.
- Combinations of prefix and separate domains (e.g.: you have custom domains for the most
  important languages, and just hos the rest on the "main" domain with prefix in the URL path).

`ievv_i18n_url` supports all these and more through:

- Swappable URL handlers where all the logic happens (this is where *these and more* comes in since you can write your own handler class).
- Template tags that use the URL handlers.
- A library that provides a superset of the functionality of what the template tags provide.
- Middleware that uses the handler to handle whatever you write a handler for.


*****
Setup
*****

Add it to ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # ...
        'ievv_opensource.ievv_i18n_url',
    ]



************
How it works
************
TODO

The handlers
============
TODO


The middleware
==============
TODO


******************************************
A warning about session based translations
******************************************
We provide support for session based translations, BUT it is not fully supported.
Things like generating an URL for a specific languagecode, or finding the translation
for the current URL in a different languagecode is NOT possible to do in a safe manner.

The reason for this limitation is that ALL translations live at the same URL, and the
only way to safely change the languagecode is to HTTP POST a change to the languagecode.
You may want to implement a handler that ignores this and actually provides full support
with session based translations. This will require some kind of redirect view
that changes the session language from a HTTP GET request.

Our recommendation is to NOT use session based translations, and instead use a URL path
or domain based translation handler.