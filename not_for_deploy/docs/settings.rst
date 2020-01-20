########
Settings
########


*************************
ievvtasks_dump_db_as_json
*************************

.. setting:: IEVVTASKS_DUMPDATA_DIRECTORY

IEVVTASKS_DUMPDATA_DIRECTORY
============================
The directory where we put dumps created by the ``ievvtasks_dump_db_as_json``
management command. Typically, you put something like this in your develop settings::

    THIS_DIR = os.path.dirname(__file__)

    IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


.. setting:: IEVVTASKS_DUMPDATA_ADD_EXCLUDES

IEVVTASKS_DUMPDATA_ADD_EXCLUDES
===============================
Use this setting to add models and apps to exclude from the dumped json. We exclude:

- contenttypes
- auth.Permission
- sessions.Session

By default, and we exclude ``thumbnail.KVStore`` by default if ``sorl.thumbnail`` is
in installed apps, and the ``THUMBNAIL_KVSTORE`` setting is configured to use the
database (``sorl.thumbnail.kvstores.cached_db_kvstore.KVStore``).

Example::

    IEVVTASKS_DUMPDATA_ADD_EXCLUDES = [
        'auth.Group',
        'myapp.MyModel',
    ]



.. setting:: IEVVTASKS_DUMPDATA_EXCLUDES

IEVVTASKS_DUMPDATA_EXCLUDES
===========================
If you do not want to get the default excludes, you can use this instead of
:setting:`IEVVTASKS_DUMPDATA_ADD_EXCLUDES` to specify exactly what to
exclude.


**********************
ievvtasks_makemessages
**********************


.. setting:: IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES

IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES
=====================================
The languages to build translations for. Example::

    IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES = ['en', 'nb']


.. setting:: IEVVTASKS_MAKEMESSAGES_IGNORE

IEVVTASKS_MAKEMESSAGES_IGNORE
=============================
The patterns to ignore when making translations. Defaults to::

    IEVVTASKS_MAKEMESSAGES_IGNORE = [
        'static/*'
    ]


.. setting:: IEVVTASKS_MAKEMESSAGES_DIRECTORIES

IEVVTASKS_MAKEMESSAGES_DIRECTORIES
==================================
Directories to run makemessages and compilemessages in. Defaults to a list with the
current working directory as the only item. The use case for this setting is if you
have your translation files split over multiple apps or directories. Then you can use
this setting to specify the parent directories of all your ``locale`` directories.

Lets say you have this structure::

    myproject/
        usersapp/
            locale/
        untranslatedapp/
        themeapp/
            locale/

You can then configure ``ievv makemessages`` and ``ievv compilemessages`` to
build the translations in ``myproject.usersapp`` and ``myproject.themeapp`` with
the following setting::

    IEVVTASKS_MAKEMESSAGES_DIRECTORIES = [
        'myproject/usersapp',
        'myproject/themeapp',
    ]

Just adding strings to ``IEVVTASKS_MAKEMESSAGES_DIRECTORIES`` is just a shortcut.
You can add dicts instead::

    IEVVTASKS_MAKEMESSAGES_DIRECTORIES = [
        {
            'directory': 'myproject/usersapp',
        },
        {
            'directory': 'myproject/themeapp',
            'python': True,  # Build python translations
            'javascript': True,  # Build javascript translations
            # 'javascript_ignore': ['something/*'],  # Override IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE for the directory
            # 'python_ignore': ['something/*'],  # Override IEVVTASKS_MAKEMESSAGES_IGNORE for the directory
        }
    ]



.. setting:: IEVVTASKS_MAKEMESSAGES_BUILD_JAVASCRIPT_TRANSLATIONS

IEVVTASKS_MAKEMESSAGES_BUILD_JAVASCRIPT_TRANSLATIONS
====================================================
Set this to ``True`` if you want to built translations for javascript code. Defaults to ``False``.


.. setting:: IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE

IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE
========================================
The patterns to ignore when making javascript translations. Defaults to::

    IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE = [
        'node_modules/*',
        'bower_components/*',
        'not_for_deploy/*',
    ]


.. setting:: IEVVTASKS_MAKEMESSAGES_PRE_MANAGEMENT_COMMANDS

IEVVTASKS_MAKEMESSAGES_PRE_MANAGEMENT_COMMANDS
==============================================
Iterable of managemement commands to run before running makemessages. Example::

    IEVVTASKS_MAKEMESSAGES_PRE_MANAGEMENT_COMMANDS = [
        {
            'name': 'ievvtasks_buildstatic',
            'options': {
                'includegroups': ['i18n']
            }
        }
    ]

Defaults to empty list.

The items in the iterable can be one of:

- A string with the name of a management command (for commands without any
  arguments or options).
- A dict with ``name``, ``args``, and ``options`` keys. The
  ``name`` key is required, but ``args`` and ``options`` are
  optional. ``args`` and ``options`` is just forwarded to
  ``django.core.management.call_command``.


.. setting:: IEVVTASKS_MAKEMESSAGES_EXTENSIONS

IEVVTASKS_MAKEMESSAGES_EXTENSIONS
=================================
Extensions to look for strings marked for translations in
normal python/django code (for the ``django`` --domain for makemessages).

Defaults to ``['py', 'html', 'txt']``.


.. setting:: IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_EXTENSIONS

IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_EXTENSIONS
============================================
Extensions to look for strings marked for translations in
javascript code (for the ``djangojs`` --domain for makemessages).

Defaults to ``['js']``.



**************
ievvtasks_docs
**************


.. setting:: IEVVTASKS_DOCS_DIRECTORY

IEVVTASKS_DOCS_DIRECTORY
========================
The directory where your sphinx docs resides (the directory where you have your sphinx ``conf.py``).
Defaults to ``not_for_deploy/docs/``.

.. setting:: IEVVTASKS_DOCS_BUILD_DIRECTORY

IEVVTASKS_DOCS_BUILD_DIRECTORY
==============================
The directory where your sphinx docs should be built.
Defaults to ``not_for_deploy/docs/_build``.



************************
ievvtasks_recreate_devdb
************************

.. setting:: IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS

IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS
=================================================
Iterable of managemement commands to after creating/restoring and migrating the
database in ``ievv recreate_devdb``. Example::

    IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS = [
        {
            'name': 'createsuperuser',
            'args': ['test@example.com'],
            'options': {'verbosity': 3}
        },
        'ievvtasks_set_all_passwords_to_test',
    ]

The items in the iterable can be one of:

- A string with the name of a management command (for commands without any
  arguments or options).
- A dict with ``name``, ``args``, and ``options`` keys. The
  ``name`` key is required, but ``args`` and ``options`` are
  optional. ``args`` and ``options`` is just forwarded to
  ``django.core.management.call_command``.


*****************
ievv_tagframework
*****************


.. setting:: IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES

IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES
=================================
The legal values for :obj:`ievv_opensource.ievv_tagframework.models.Tag.tagtype`.

Example::

    IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES = [
        ('', ''),
        ('mytype', 'My tag type'),
    ]


***********
ievv devrun
***********

.. setting:: IEVVTASKS_DEVRUN_RUNNABLES

IEVVTASKS_DEVRUN_RUNNABLES
==========================
Dict mapping ``ievv devrun`` target names to :class:`ievv_opensource.utils.ievvdevrun.config.RunnableThreadList`
objects. Must contain the ``"default"`` key.

Documented in :doc:`ievvtask_devrun`.


*******************
ievv_batchframework
*******************

.. setting:: IEVV_BATCHFRAMEWORK_ALWAYS_SYNCRONOUS

IEVV_BATCHFRAMEWORK_ALWAYS_SYNCRONOUS
=====================================
If this is ``True``, all actions will be executed syncronously. Read more about
this in :ref:`ievv_batchframework_develop_asyncronous`.


********
ievv_sms
********

.. setting:: IEVV_SMS_DEFAULT_BACKEND_ID

IEVV_SMS_DEFAULT_BACKEND_ID
===========================
The default backend ID to use for SMS sending. Example::

    IEVV_SMS_DEFAULT_BACKEND_ID = 'debugprint'


*******
ievv_db
*******

...setting:: IEVV_DB_POSTGRES_COLLATION

IEVV_DB_POSTGRES_COLLATION
==========================
The collation to use for Django order_by that :func:`ievv_opensource.ievv_db.postgres.collate_utils.collate`
uses as fallback if not passed as a parameter. Example::

Example setting the default collation in settings::

    IEVV_DB_POSTGRES_COLLATION = 'en_US.UTF-8'


Example usage in query::
    from ievv_opensource.ievv_db.postgres.collate_util import collate

    # Ascending order
    ExampleModel.objects.order_by(collate('some_field'))

    # Descending order
    ExampleModel.objects.order_by(collate('-some_field'))


*****
utils
*****

.. setting:: IEVV_SLUGIFY_CHARACTER_REPLACE_MAP

IEVV_SLUGIFY_CHARACTER_REPLACE_MAP
==================================
Custom character replacement map for the ``ievv_slugify`` function



.. setting:: IEVV_COLORIZE_USE_COLORS

IEVV_COLORIZE_USE_COLORS
========================
Colorize output from :func:`ievv_opensource.utils.ievv_colorize.colorize`? Defaults
to ``True``.


.. setting:: IEVV_VALID_REDIRECT_URL_REGEX

IEVV_VALID_REDIRECT_URL_REGEX
=============================
Valid redirect URLs for :doc:`utils.validate_redirect_url`.

Defaults to ``^/.*$``, which means that only urls without domain is allowed by default.


Example for only allowing redirect urls that does not contain a domain, or
redirect urls within the example.com domain::

    IEVV_VALID_REDIRECT_URL_REGEX = r'^(https?://example\.com/|/).*$'

.. warning:: Do not use ``^https://example\.com.*$`` (no / after the domain). This
    can potentially lead to attacks using subdomains. ``^https://example\.com.*$`` would
    allow ``example.com.spamdomain.io/something``, but ``^https://example\.com/.*$`` would
    not allow this.
