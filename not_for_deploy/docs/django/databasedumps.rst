#################################
Using and creating database dumps
#################################

We use dumpscript_
from the django-extentions Django app to create our test data. We already have data, so
unless you want to add more data, you do not need to know anything more than how
to run a Django management task or a fabric task.

.. note:: This was first described in :issue:`4`.


***********************
Importing the test data
***********************
The easiest method of importing the test database is to use the ``recreate_testdb`` Fabric task::

    $ cd djangoproject/
    $ fab recreate_testdb

.. warning:: This will destroy your current database.


A slighly more low level method is to use the management command::

    $ python manage.py runscript ievv_opensource_project.develop.dumps.core.data

This does exactly the same as the management command, but it does not destroy
and re-initialize the database for you first.



**************************
Users in the test database
**************************
After importing the test data, you will have some new users. Login to the Django admin UI (http://localhost:8000) with::

    user: grandma@example.com
    password: test

and select Users to list all users. The password of all users are ``test``.



************
Add new data
************
To add new data, you just need to do add data to the database manually, or programmatically.

Adding data manually (I.E.: Using the Django admin UI)
======================================================
To add data manually, you should first run thr ``recreate_testdb`` management
command to make sure you start out with the current up-to-date dataset. Then you
can use the web-UI or the Django shell to add data. Finally, run::

    $ fab dump_current_db_to_dumpscript_datafile


Adding data programmatically
============================
Adding data programmatically must be done in
``src/ievv_opensource_project/develop/dumps/core/import_helper.py``. See the comment at
the top of ``src/ievv_opensource_project/develop/dumps/core/data.py`` for information
about how ``import_helper`` works.


.. _dumpscript: http://django-extensions.readthedocs.org/en/latest/dumpscript.html
