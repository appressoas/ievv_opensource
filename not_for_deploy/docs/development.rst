#################
Development guide
#################


************************
Install the requirements
************************
Install the following:

#. Python
#. PIP_
#. VirtualEnv_
#. pipenv_


********************************
Install development requirements
********************************

Install the development requirements::

    $ pipenv install --dev


.. _enable-virtualenv:

.. note::

    The commands below assume you are in the virtualenv. You activate the virtualenv with::

        $ pipenv shell

    You can also run all the commands with::

        $ pipenv run <command>


**************
Build the docs
**************
:ref:`Enable the virtualenv <enable-virtualenv>`, and run::

    $ ievv docs --build --open


*****************************
Create a development database
*****************************
:ref:`Enable the virtualenv <enable-virtualenv>`, and run::

    $ ievv recreate_devdb

This creates a superuser with::

    username: grandma
    password: test


*************
Running tests
*************
To run the tests, we need to use a different settings file. We tell ievvtasks to
do this using the ``DJANGOENV`` environent variable::

    $ DJANGOENV=test python manage.py test


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
.. _pipenv: https://pipenv-fork.readthedocs.io/en/latest/


************************
Adding more dependencies
************************
Just add dependencies as normal with pipenv, BUT make sure you run::

    $ pipenv lock -r > requirements.txt

when you merge into master before you push IF you add any non-dev dependencies. This
is because readthedocs requires ``requirements.txt`` to build.
