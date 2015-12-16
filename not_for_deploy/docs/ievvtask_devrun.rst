#############################################################
`ievv devrun` --- All your development servers in one command
#############################################################

The ``ievv devrun`` command makes it easy to run (start/stop) all your development
servers with a single command. It uses multithreading, background processes
to run all your servers in a single blocking process that stops all the
processes when ``CTRL-C`` is hit.


***************
Getting started
***************
First of all, make sure you have the following in your ``INSTALLED_APPS`` setting::

    'ievv_opensource.ievvtasks_common',
    'ievv_opensource.ievvtasks_development',

Next, you need to configure what to run when you run ``ievv devrun``. You
do this with the ``IEVVTASKS_DEVRUN_RUNNABLES``-setting. For this
example, we will setup *Django runserver* and *Django dbdev database server*::

    IEVVTASKS_DEVRUN_RUNNABLES = ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread()
    )

With the configured, you can run::

    $ ievv devrun

Hit ``CTRL-C`` to stop both the servers.

to start both the Django development server and your
`Django dbdev <https://github.com/espenak/django_dbdev>`_ database.


****************
Custom runnables
****************
We bundle a fairly limited set of runnables, but adding one is really easy.
Check out the docs for:

- :class:`ievv_opensource.utils.ievvdevrun.runnables.base.ShellCommandRunnableThread`
- :class:`ievv_opensource.utils.ievvdevrun.runnables.base.AbstractRunnableThread`


*****************
Bundled runnables
*****************

Overview
========

.. currentmodule:: ievv_opensource.utils.ievvdevrun.runnables

.. autosummary::

   base.AbstractRunnableThread
   base.ShellCommandRunnableThread
   django_runserver.RunnableThread
   dbdev_runserver.RunnableThread


Details
=======

.. currentmodule:: ievv_opensource.utils.ievvdevrun.runnables.base
.. automodule:: ievv_opensource.utils.ievvdevrun.runnables.base

.. currentmodule:: ievv_opensource.utils.ievvdevrun.runnables.django_runserver
.. automodule:: ievv_opensource.utils.ievvdevrun.runnables.django_runserver

.. currentmodule:: ievv_opensource.utils.ievvdevrun.runnables.dbdev_runserver
.. automodule:: ievv_opensource.utils.ievvdevrun.runnables.dbdev_runserver


*************
Low level API
*************

.. currentmodule:: ievv_opensource.utils.ievvdevrun.config
.. automodule:: ievv_opensource.utils.ievvdevrun.config
