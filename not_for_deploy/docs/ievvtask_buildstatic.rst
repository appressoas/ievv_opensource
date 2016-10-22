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
First of all, make sure you have the following in your ``INSTALLED_APPS`` setting::

    'ievv_opensource.ievvtasks_common',

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


*********************************
NPM packages and ievv buildstatic
*********************************

How ievv buildstatic interracts with package.json
=================================================
Many of the ievv buildstatic plugins install their own npm packages,
so they will modify ``package.json`` if needed. Most plugins
do not specify a specific version of a package, but they will
not override your versions if you specify them in ``package.json``.


Yarn or NPM?
============
ievv buildstatic uses ``yarn`` by default, but you can configure it to
use ``npm`` with the following settings::

    IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
        ievvbuildstatic.config.App(
            appname='myapp',
            version='1.0.0',
            installers_config={
                'npm': {
                    'installer_class': ievvbuildstatic.installers.npm.NpmInstaller
                }
            },
            plugins=[
                # ...
            ]
        )
    )


*******************************
Working with npm packages guide
*******************************

.. note:: You can create your ``package.json`` manually, using ``npm init``/``yarn init``. If
    you do not create a package.json, ievv buildstatic will make one for you if you use any
    plugins that require npm packages.

You work with npm/yarn just like you would for any javascript project.
The package.json file must be in::

    <django appname>/staticsources/<django appname>/package.json

So you should be in ``<django appname>/staticsources/<django appname>/`` when
running npm or yarn commands.


Example
=======
1. Create the ``staticsources/myapp/`` directory in your django app.
   Replace myapp with your django app name.
2. Create  ``staticsources/myapp/scripts/javascript/app.js``.
3. Configure ievv buildstatic with the following in your django settings::

    IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
        ievvbuildstatic.config.App(
            appname='myapp',
            version='1.0.0',
            plugins=[
                ievvbuildstatic.browserify_jsbuild.Plugin(
                    sourcefile='app.js',
                    destinationfile='app.js',
                ),
            ]
        )
    )

4. Run ``ievv buildstatic`` to build this app. This will create a ``package.json`` file.
5. Lets add momentjs as a dependency::

    $ cd /path/to/myapp/staticsources/myapp/
    $ yarn add momentjs

6. ... and so on ...



*******
Plugins
*******

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic

.. autosummary::

   pluginbase.Plugin
   cssbuildbaseplugin.AbstractPlugin
   sassbuild.Plugin
   lessbuild.Plugin
   mediacopy.Plugin
   bowerinstall.Plugin
   npminstall.Plugin
   browserify_jsbuild.Plugin
   browserify_babelbuild.Plugin
   browserify_reactjsbuild.Plugin
   autosetup_jsdoc.Plugin
   autosetup_esdoc.Plugin


Details
=======

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.pluginbase
.. automodule:: ievv_opensource.utils.ievvbuildstatic.pluginbase

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.cssbuildbaseplugin
.. automodule:: ievv_opensource.utils.ievvbuildstatic.cssbuildbaseplugin

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.sassbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.sassbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.lessbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.lessbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.mediacopy
.. automodule:: ievv_opensource.utils.ievvbuildstatic.mediacopy

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.bowerinstall
.. automodule:: ievv_opensource.utils.ievvbuildstatic.bowerinstall

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.npminstall
.. automodule:: ievv_opensource.utils.ievvbuildstatic.npminstall

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.browserify_jsbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.browserify_jsbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.browserify_babelbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.browserify_babelbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.browserify_reactjsbuild
.. automodule:: ievv_opensource.utils.ievvbuildstatic.browserify_reactjsbuild

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.autosetup_jsdoc
.. automodule:: ievv_opensource.utils.ievvbuildstatic.autosetup_jsdoc

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.autosetup_esdoc
.. automodule:: ievv_opensource.utils.ievvbuildstatic.autosetup_esdoc


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


*****
Utils
*****

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.utils

.. automodule:: ievv_opensource.utils.ievvbuildstatic.utils

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.filepath

.. automodule:: ievv_opensource.utils.ievvbuildstatic.filepath



**********
Installers
**********

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers

.. autosummary::

   base.AbstractInstaller
   npm.NpmInstaller
   yarn.YarnInstaller


Details
=======

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers.base
.. automodule:: ievv_opensource.utils.ievvbuildstatic.installers.base

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers.npm
.. automodule:: ievv_opensource.utils.ievvbuildstatic.installers.npm

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.installers.yarn
.. automodule:: ievv_opensource.utils.ievvbuildstatic.installers.yarn


*************
Low level API
*************

.. currentmodule:: ievv_opensource.utils.ievvbuildstatic.watcher
.. automodule:: ievv_opensource.utils.ievvbuildstatic.watcher
