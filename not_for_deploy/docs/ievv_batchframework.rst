########################################################
`ievv_batchframework` --- Framework for batch/bulk tasks
########################################################

The intention of this module is to make it easier to write code
for background tasks and some kinds of bulk operations.


*************
Configuration
*************
Add the following to your ``INSTALLED_APPS``-setting:

    'ievv_opensource.ievv_batchframework.apps.BatchOperationAppConfig'



**********************************
Batchregistry - the high level API
**********************************



************************
Recommended Celery setup
************************

Install Redis
=============
Redis is very easy to install and use, and it is one of the recommended
broker and result backends for Celery, so we recommend that you use this
when developing with Celery. You may want to use the Django database instead,
but that leaves you with a setup that is further from a real production environment,
and using Redis is very easy if you use *ievv devrun* as shown below.

On Mac OSX, you can install redis with Homebrew using::

    $ brew install redis

and most linux systems have Redis in their package repository. For other
systems, go to http://redis.io/, and follow their install guides.



Configure Celery
================

First, you have to create a Celery Application for your project.
Create a file named ``celery.py`` within a module that you know is
loaded when Django starts. The safest place is in the root of your
project module. So if you have::

    myproject/
        __init__.py
        myapp/
            __init__.py
            models.py
        mysettings/
            settings.py

You should add the celery configuration in ``myproject/celery.py``. The rest of this
guide will assume you put it at this location.


Put the following code in ``myproject/celery.py``::

    from __future__ import absolute_import
    import os
    from celery import Celery

    # Ensure this matches your
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    # The ``main``-argument is used as prefix for celery task names.
    app = Celery(main='myproject')

    # We put all the celery settings in out Django settings so we use
    # this line to load Celery settings from Django settings.
    # You could also add configuration for celery directly in this
    # file using app.conf.update(...)
    app.config_from_object('django.conf:settings')

    # This debug task is only here to make it easier to verify that
    # celery is working properly.
    @app.task(bind=True)
    def debug_add_task(self, a, b):
        print('Request: {0!r} - Running {} + {}, and returning the result.'.format(
            self.request, a, b))
        return a + b


And put the following code in ``myproject/__init__.py``::

    from __future__ import absolute_import

    # This will make sure the Celery app is always imported when
    # Django starts so that @shared_task will use this app.
    from .celery import app as celery_app


Add the following to your Django settings::

    # Celery settings
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Europe/Oslo'  # Change to your preferred timezone!
    CELERY_IMPORTS = [
        'ievv_opensource.ievv_batchframework.celery_tasks',
    ]
    CELERYD_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] ' \
                              '[%(name)s] ' \
                              '[%(task_name)s(%(task_id)s)] ' \
                              '%(message)s'

    # ievv_batchframework settings
    IEVV_BATCHFRAMEWORK_CELERY_APP = 'myproject.celery_app'


Setup :doc:`ievvtask_devrun`, and add ``ievvdevrun.runnables.redis_server.RunnableThread()``
and ``
to your ``IEVVTASKS_DEVRUN_RUNNABLES``. You should end up with something like this::

    IEVVTASKS_DEVRUN_RUNNABLES = {
        'default': ievvdevrun.config.RunnableThreadList(
            # ievvdevrun.runnables.dbdev_runserver.RunnableThread(),  # Uncomment if using django_dbdev
            ievvdevrun.runnables.django_runserver.RunnableThread(),
            ievvdevrun.runnables.redis_server.RunnableThread(),
            ievvdevrun.runnables.celery_worker.RunnableThread(app='myproject'),
        ),
    }


At this point, you should be able to run::

    $ ievv devrun

to start the Django server, redis and the celery worker. To test that everything is working:

1. Take a look at the output from ``ievv devrun``, and make sure that your ``debug_add_task``
   (from celery.py) is listed as a task in the ``[tasks]`` list printed by the celery worker
   on startup. If it is not, this probably means you did not put the code in the
   ``myproject/__init__.py`` example above in a place that Django reads at startup. You may
   want to try to move it into the same module as your ``settings.py`` and restart
   ``ievv devrun``.
2. Start up the django shell and run the ``debug_add_task``::

        $ python manage.py shell
        >>> from myproject.celery import debug_add_task
        >>> result = debug_add_task.delay(10, 20)
        >>> result.wait()
        30

   If this works, Celery is configured correctly.


*****************
Batchregistry API
*****************

.. currentmodule:: ievv_opensource.ievv_batchframework.batchregistry

.. automodule:: ievv_opensource.ievv_batchframework.batchregistry


************************
The BatchOperation model
************************
The BatchOperation model is at the hearth of ``ievv_batchframework``.
Each time you start a batch process, you create an object
of :class:`ievv_opensource.ievv_batchframework.models.BatchOperation`
and use that to communicate the status, success/error data and
other metadata about the batch operation.


Asyncronous operations
======================
An asyncronous operation is the most common use case for
the BatchOperation model. It is used to track a task
that is handled (E.g.: completed) by some kind of asyncronous
service such as a cron job or a Celery task.

Lets say you have want to send an email 15 minutes after
a blog post has been created unless the user cancels the email
sending within within 15 minutes. You would then need to:

- Create a BatchOperation object each time a blog post
  is created.
- Use some kind of batching service, like Celery, to poll
  for BatchOperation objects that asks it to send out email.
- Delete the BatchOperation if a user clicks "cancel"
  within 15 minutes of the creation timestamp.

The code for this would look something like this::

    from ievv_opensource.ievv_batchframework.models import BatchOperation

    myblogpost = Blog.objects.get(...)
    BatchOperation.objects.create_asyncronous(
        context_object=myblogpost,
        operationtype='new-blogpost-email')
    # code to send the batch operation to the batching service (like celery)
    # with a 15 minute delay, or just a service that polls for
    # BatchOperation.objects.filter(operationtype='new-blogpost-email',
    #                               created_datetime__lt=timezone.now() - timedelta(minutes=15))


    # The batching service code
    def my_batching_service(...):
        batchoperation = BatchOperation.objects.get(...)
        batchoperation.mark_as_running()
        # ... send out the emails ...
        batchoperation.finish()


    # In the view for cancelling email sending
    BatchOperation.objects\
        .filter(operationtype='new-blogpost-email',
                context_object=myblogpost)\
        .remove()


Syncronous operations
=====================
You may also want to use BatchOperation for syncronous operations.
This is mainly useful for complex bulk create and bulk update operations.

Lets say you have Game objects with a one-to-many relationship to Player
objects with a one-to-many relationship to Card objects. You want to start all
players in a game with a card. How to you batch create all the players with a
single card?

You can easily batch create players with ``bulk_create``, but you can not
batch create the cards because they require a Player. So you need to a way
of retrieving the players you just batch created.

If you create a BatchOperation with
:obj:`~ievv_opensource.ievv_batchframework.models.BatchOperation.context_object`
set to the Game, you will get a unique identifier for the operation (the id of
the BatchOperation). Then you can set that identifier as an attribute on all
the batch-created Player objects (preferrably as a foreign-key), and retrieve
the batch created objects by filtering on the id of the BatchOperation.
After this, you can iterate through all the created Player objects, and create a
list of Card objects for your batch create operation for the cards.

Example::

    game = Game.objects.get(...)
    batchoperation = BatchOperation.objects.create_syncronous(
        context_object=game)

    players = []
    for index in range(1000):
        player = Player(
            game=game,
            name='player{}'.format(index),
            batchoperation=batchoperation)
        players.append(player)
    Player.objects.bulk_create(players)
    created_players = Player.objects.filter(batchoperation=batchoperation)

    cards = []
    available_cards = [...]  # A list of available card IDs
    for player in created_players:
        card = Card(
            player=player,
            cardid=random.choice(available_cards)
        )
        cards.append(card)
    Card.objects.bulk_create(cards)
    batchoperation.finish()

As you can see in the example above, instead of having to perform 2000 queries
(one for each player, and one for each card), we now only need 5 queries
no matter how many players we have (or a few more on database servers that can
not bulk create 1000 items at a time).


**************
Data model API
**************

.. currentmodule:: ievv_opensource.ievv_batchframework.models

.. automodule:: ievv_opensource.ievv_batchframework.models
