from django.conf import settings
from django.utils.translation import get_language_info


class AbstractHandler:
    """
    Base class for `ievv_i18n_url` handlers.
    """
    def __init__(self, request):
        """

        Args:
            request (django.http.HttpRequest): Django http request object, or a
                :class:`ievv_opensource.ievv_i18n_url.ievv_i18n_url_utils.FakeHttpRequest` object.
        """
        self.request = request

    def is_default_languagecode(self, languagecode):
        """Is the provided languagecode the default language code?

        Note that this may be per domain etc. depending on the handler class. This returning ``True``
        really just means that it is the default for the ``request``, not the default for the
        entire application.

        Args:
            languagecode (str): Language code.

        Returns:
            bool: True if the provided languagecode is the default.
        """
        return languagecode == self.get_default_languagecode()

    def get_default_languagecode(self):
        """Get the default language code.

        Note that this may be per domain etc. depending on the handler class.
        This just returns the default for the ``request``, which normally means
        default for the entire application or default for the current domain.

        Defaults to ``settings.LANGUAGE_CODE``.

        Returns:
            str: Default languagecode.
        """
        return self.request.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE

    def get_current_languagecode(self):
        """Get the current languagecode.

        Defaults to ``request.LANGUAGE_CODE``, which will just work if
        you use the middleware provided by ``ievv_i18n_url``.

        Returns:
            str: The current languagecode.
        """
        return getattr(self.request, 'LANGUAGE_CODE', None) or self.get_default_languagecode()

    def get_supported_languagecodes(self):
        """Get supported language codes.

        Defaults to the language codes in ``settings.LANGUAGES``.

        Returns:
            set: A set of the supported language codes.
        """
        return {l[0] for l in settings.LANGUAGES}

    def is_supported_languagecode(self, languagecode):
        """Is the provided languagecode a supported languagecode?

        Args:
            languagecode (str): Language code.

        Returns:
            bool: True if the provided languagecode is supported.
        """
        return languagecode in self.get_supported_languagecodes()

    def get_translated_label_for_languagecode(self, languagecode):
        """Get the translated label for the languagecode (the name of the language)
        in the currently active language.

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is typically used in subclasses that override :meth:`~.AbstractHandler.get_label_for_languagecode`
        and change to translated labels by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Translated label for the languagecode.
        """
        language_info = get_language_info()
        return language_info['name_translated']

    def get_untranslated_label_for_languagecode(self, languagecode):
        """Get the untranslated label for the languagecode (the name of the language).

        Should return a label for the languagecode in a commonly used
        language that most users of your site will understand.

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is the what the default implementation of :meth:`~.AbstractHandler.get_label_for_languagecode`
        uses.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Unstranslated label for the languagecode.
        """
        language_info = get_language_info()
        return language_info['name']

    def get_local_label_for_languagecode(self, languagecode):
        """Get the local label for the languagecode (the name of the language in that language).

        This defaults to the english name for the language fetched
        via ``django.utils.translation.get_language_info()``.

        This is typically used in subclasses that override :meth:`~.AbstractHandler.get_label_for_languagecode`
        and change to labels in the native language by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Local label for the languagecode.
        """
        language_info = get_language_info()
        return language_info['name_local']

    def get_label_for_languagecode(self, languagecode):
        """Get the label for the languagecode (the name of the language).

        Defaults to using :meth:`~.AbstractHandler.get_local_label_for_languagecode`.
        I.e.: We use the native/local translation of the language name for labels for
        language labels by default.

        Args:
            languagecode (str): Language code.

        Returns:
            str: Label for the languagecode.
        """
        return self.get_local_label_for_languagecode(languagecode)

    ##################################################
    #
    # Methods designed to be overridden in subclasses:
    #
    ##################################################

    def is_translatable_urlpath(path):
        """Is the provided URL path translatable?

        We default to consider the paths in settings.MEDIA_URL and settings.STATIC_URL as untranslatable.

        If this returns ``False``, the middleware will use the default translation when serving
        the path.

        If you subclass this, you should not write code that parses the querystring part of the
        path. This will not work as intended (will not work the same everywhere) since the middleware
        does not call this with the querystring included, but other code using this may pass in the path
        with the querystring.

        Args:
            path (str): An URL path (e.g: ``/my/path``, ``/my/path?a=1&b=2``, etc.)
        Returns:
            bool: Is the provided URL translatable?
        """
        if settings.STATIC_URL and path.startswith(settings.STATIC_URL):
            return False
        if settings.settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
            return False
        return True

    def get_icon_cssclass_for_languagecode(self, languagecode):
        """Get an icon CSS class for the language code.

        This is typically implemented on a per app basis. I.e.: The application
        creates a subclass of one of the built-in handlers and override this
        to provide icons for their supported languages. This is provided as
        part of the handler to make it possible to generalize things like
        rendering language selects with icons.

        This icon must be possible to use in HTML like this::

            <span class="ICON_CSS_CLASS_HERE"></span>

        Args:
            languagecode (str): Language code.

        Returns:
            str: Icon css class
        """
        return None

    def get_icon_svg_image_url_for_languagecode(self, languagecode):
        """Get an icon SVG image URL for the language code.

        This is typically implemented on a per app basis. I.e.: The application
        creates a subclass of one of the built-in handlers and override this
        to provide icons for their supported languages. This is provided as
        part of the handler to make it possible to generalize things like
        rendering language selects with icons.

        Args:
            languagecode (str): Language code.

        Returns:
            str: SVG image URL.
        """
        return None

    def build_absolute_url(self, path, languagecode=None):
        """Build absolute uri for the provided path within the provided languagecode.

        MUST be implemented in subclasses.

        NOTE: Session based handlers will ignore the languagecode argument and just return
        the URL for the default translation. This is because all their translations live at the same URL.
        See the _A warning about session based translations_ in the docs for more details.

        Args:
            path (str): The path (same format as HttpRequest.get_full_path()
                returns - e.g: ``"/my/path?option1&option2"``)
            languagecode (str, optional): The languagecode to build the URI for. Defaults to None, which
                means we build the URI within the current languagecode.
        """
        raise NotImplementedError()

    def transform_url_to_languagecode(self, uri, languagecode):
        """Transform the provided uri into the "same" uri, but in the provided languagecode.

        MUST be implemented in subclasses.

        NOTE: This is not possible to implement in a safe
        manner for session based handlers (I.e.: multiple translation live at the same URI),
        so for these kind of handler this method will just return the provided `uri`.
        See the _A warning about session based translations_ in the docs for more details.

        Args:
            uri (str): The URI to transform.
            languagecode (str, optional): The languagecode to transform the URI into.
        """
        raise NotImplementedError()

    def find_current_languagecode(self):
        """Find the current languagecode.

        Used by the middleware provided by `ievv_i18n_url` find the current language code
        and set it on the current request.

        DO NOT USE THIS - it is for the middleware. Use :meth:`~.AbstractHandler.get_current_languagecode`.

        MUST be overridden in subclasses.

        If this returns None, it means that we should use the default languagecode. I.e.: Do not handle
        fallback to default languagecode when implementing this method in subclasses - just return None.

        Returns:
            str: The current languagecode or None (None means default languagecode is detected).
        """
        raise NotImplementedError()

    def find_default_languagecode(self):
        """Find the current languagecode.

        Used by the middleware provided by `ievv_i18n_url` to find the current language code,
        activate the translation for it and set it on the current request as
        ``request.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE``.

        DO NOT USE THIS - it is for the middleware. Use :meth:`~.AbstractHandler.get_default_languagecode`.

        Returns:
            str: The default languagecode. Defaults to ``settings.LANGUAGE_CODE``.
        """
        return settings.LANGUAGE_CODE

    def get_translation_to_activate_for_languagecode(self, languagecode):
        """Find the current languagecode.

        Used by the middleware provided by `ievv_i18n_url` to activate the translation for the
        provided languagecode.

        This is here to make it possible for applications to have languages that has their
        own domains or URLs, but show translations from another language code. E.g.:
        you may have content in a language, but be OK with translation strings from another language.

        Returns:
            str: The languagecode to activate with the django translation system for the provided ``languagecode``.
            Defaults to the provided ``languagecode``.
        """
        return languagecode
