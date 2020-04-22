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

Things this handle that the built-in locale URL support in Django does not handle:

- Different default/fallback language per domain.
- Support for domains to define the languagecode.
- Locale aware URL reversing (e.g.: link to a page in a specific language).


*****
Setup
*****

Add it to settings::

   INSTALLED_APPS = [
      # ...
      'ievv_opensource.ievv_i18n_url',
   ]

   MIDDLEWARE = [
      # ...
      # Instead of django.middleware.locale.LocaleMiddleware, or any other LocaleMiddleware,
      'ievv_opensource.ievv_i18n_url.middleware.LocaleMiddleware'
   ]

   # Fallback base URL - used everywhere that we can not determine the "current" domain (management scripts that does not specify a base url etc).
   IEVV_I18N_URL_FALLBACK_BASE_URL = https://mydomain.com/

   # The handler class - see further down for the available handler classes
   IEVV_I18N_URL_HANDLER = 'ievv_opensource.ievv_i18n_url.handlers.UrlpathPrefixHandler'


In your urls.py, wrap your URLs with i18n_patterns()::

   from ievv_opensource.ievv_i18n_url import i18n_url_utils

   # Instead of:
   # urlpatterns = [
   #     url(r'^my/view$', myview),
   #     url(r'^another/view$', anotherview),
   # ]

   # Wrap it in i18n_urlpatterns like this:
   urlpatterns = i18n_url_utils.i18n_patterns(
      url(r'^my/view$', myview),
      url(r'^another/view$', anotherview),
   )

.. warning::

   You should not have ANY urls that are not wrapped with i18n_patterns - this will just make
   the middleware and handlers work in an undeterministic manner. If you want to exclude URLs
   from being translated, create a subclass of your handler and override
   :meth:`ievv_opensource.ievv_i18n_url.handlers.AbstractHandler.is_translatable_urlpath`.


************
How it works
************
A very high level overview of how it works is that we have swappable handlers that decide what the current
language is based on information they get from the request and URL.


The handlers
============
The handlers serve two puposes:
- They have some classmehods that the LocaleMiddleware uses to set the current language. I.e.: The handlers
  basically implement what the middleware should do.
- They have a lot of helper methods to make it easy to work with locale aware URL schemes,
  and some methods to help generalize locale handling (such as labels and icons for languages).


The LocaleMiddleware
====================
The middleware, :class:`ievv_opensource.ievv_i18n_url.middleware.LocaleMiddleware`, is very simple. It
just calls :meth:`ievv_opensource.ievv_i18n_url.handlers.AbstractHandler.activate_languagecode_from_request`
on the configured handler, and then it sets some information about the detected language on the request:

- ``request.LANGUAGE_CODE``: Set to the languagecode we activated django translations for.
- ``request.session['LANGUAGE_CODE']``: Same value as request.LANGUAGE_CODE - this is just set for compatibility with
  code that is written explicitly for session based language selection.
- ``request.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE``: Set to the detected default language code.
- ``request.IEVV_I18N_URL_ACTIVE_LANGUAGE_CODE``: Set to the active languagecode. This is normally the same as
  request.LANGUAGE_CODE, but if :meth:`ievv_opensource.ievv_i18n_url.handlers.AbstractHandler.get_translation_to_activate_for_languagecode`
  is overridden on the handler they may differ. E.g.: Multiple languages may use the same Django translation.


Url pattern handling
====================
The :func:`ievv_opensource.ievv_i18n_url.i18n_url_utils.i18n_patterns` function that
you wrap around all your URL patterns uses a custom URL resolver that
simply gets the languagecode that the middleware set, and ignores any URL path
prefix that the handler has said that we have for the current language. E.g.:
we use the same "hack/smart solution" as the built in i18n url routing handler in Django.

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


*********
Utilities
*********

i18n_url_utils
==============

.. currentmodule:: ievv_opensource.ievv_i18n_url.i18n_url_utils
.. automodule:: ievv_opensource.ievv_i18n_url.i18n_url_utils
   :members:
   :imported-members:

base_url
========

.. currentmodule:: ievv_opensource.ievv_i18n_url.base_url
.. automodule:: ievv_opensource.ievv_i18n_url.base_url
   :members:

i18n_url_settings
=================

.. currentmodule:: ievv_opensource.ievv_i18n_url.i18n_url_settings
.. automodule:: ievv_opensource.ievv_i18n_url.i18n_url_settings
   :members:

active_i18n_url_translation
===========================

.. currentmodule:: ievv_opensource.ievv_i18n_url.active_i18n_url_translation
.. automodule:: ievv_opensource.ievv_i18n_url.active_i18n_url_translation
   :members:


*************
Template tags
*************
.. currentmodule:: ievv_opensource.ievv_i18n_url.templatetags.ievv_i18n_url_tags
.. automodule:: ievv_opensource.ievv_i18n_url.templatetags.ievv_i18n_url_tags
   :members:


********
handlers
********

UrlpathPrefixHandler
====================
.. currentmodule:: ievv_opensource.ievv_i18n_url.handlers
.. autoclass:: UrlpathPrefixHandler
  :no-members:

DjangoSessionHandler
====================
.. currentmodule:: ievv_opensource.ievv_i18n_url.handlers
.. autoclass:: DjangoSessionHandler
  :no-members:

AbstractHandler
===============
.. currentmodule:: ievv_opensource.ievv_i18n_url.handlers
.. autoclass:: AbstractHandler
   :members:


**********
Middleware
**********
.. currentmodule:: ievv_opensource.ievv_i18n_url.middleware
.. automodule:: ievv_opensource.ievv_i18n_url.middleware
   :members:
