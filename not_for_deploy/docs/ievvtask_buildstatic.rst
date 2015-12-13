################################################################
`ievv buildstatic` --- A static file builder (less, coffee, ...)
################################################################

The ``ievv buildstatic`` command is a fairly full featured
general purpose static asset builder that solves the same
general tasks as Grunt and Gulp, but in a very Django
friendly and pythonic way.

You extend the system with object oriented python programming,
and you configure the system using python classes.


***************
Getting started
***************
``ievv buildstatic`` assumes you have the sources for your
static files in the ``staticsources/<appname>/`` directory
within each Django app.

For this example, we will assume your Django app is named
``myapp``, and that it is located in ``myproject/myapp/``.

First you need to create the staticsources directory::

    $ mkdir -p myproject/myapp/staticsource/myapp/


Setup building of LESS files
============================

To kick things off, we will configure building of LESS sources
into CSS. Create ``myproject/myapp/staticsource/myapp/styles/theme.less``,
and add some styles:

.. code-block:: css

    .myclass {
        color: red;
    }

Now we need to add configurations to ``settings.py`` for building
this less file. Add the following Django setting::

    from ievv_opensource.utils import ievvbuildstatic
    IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
        ievvbuildstatic.config.App(
            appname='myapp',
            version='1.0.0',
            plugins=[
                ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ]
        ),
    )

Now run the following command in your terminal::

    $ ievv buildstatic

This should create ``myproject/myapp/static/myapp/1.0.0/styles/theme.css``.


Add media files
===============
You will probably need some media files for your styles (fonts, images, ect.).
First, put an image in ``myproject/myapp/staticsource/myapp/media/images/``,
then add the following to the ``plugins`` list in the
``IEVVTASKS_BUILDSTATIC_APPS`` Django setting::

    ievvbuildstatic.mediacopy.Plugin()

Run::

    $ ievv buildstatic

This should add your image to ``myproject/myapp/static/myapp/1.0.0/media/images/``.


Watch for changes
=================
Re-running ``ievv buildstatic`` each time you make changes is
tedious. You can watch for changes using::

    $ ievv buildstatic --watch



***************
Advanced topics
***************

Using multiple apps
===================

Using multiple apps is easy. You just add another
:class:`ievv_opensource.utils.ievvbuildstatic.config.App` to
the ``IEVVTASKS_BUILDSTATIC_APPS`` setting::

    from ievv_opensource.utils import ievvbuildstatic
    IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
        ievvbuildstatic.config.App(
            appname='myapp',
            version='1.0.0',
            plugins=[
                ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ]
        ),
        ievvbuildstatic.config.App(
            appname='anotherapp',
            version='2.3.4',
            plugins=[
                ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ]
        ),
    )


*******
Plugins
*******

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic

.. autosummary::

   pluginbase.Plugin
   lessbuild.Plugin
   mediacopy.Plugin
   bowerinstall.Plugin


Details
=======

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.pluginbase
.. automodule:: ievv_opensource.utils.ievvbuildstatic.pluginbase

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.lessbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.lessbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.mediacopy
.. automodule:: ievv_opensource.utils.ievvbuildstatic.mediacopy

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.bowerinstall
.. automodule:: ievv_opensource.utils.ievvbuildstatic.bowerinstall


************
Apps and App
************

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.config

.. autosummary::

    App
    Apps


Details
=======

.. automodule:: ievv_opensource.utils.ievvbuildstatic.config


**********
Installers
**********

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers

.. autosummary::

   base.AbstractInstaller
   npm.NpmInstaller


Details
=======

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers.base
.. automodule:: ievv_opensource.utils.ievvbuildstatic.installers.base

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers.npm
.. automodule:: ievv_opensource.utils.ievvbuildstatic.installers.npm


*************
Low level API
*************

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.watcher
.. automodule:: ievv_opensource.utils.ievvbuildstatic.watcher
