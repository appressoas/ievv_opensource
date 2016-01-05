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
a blog post has been created unless the user edits the
blog post within 15 minutes. You would then need to:

- Create a BatchOperation object each time a blog post
  is created.
- Use some kind of batching service, like Celery, to poll
  for BatchOperation objects that asks it to send out email.
- Delete the BatchOperation if a user edits the blog post
  within 15 minutes of the creation timestamp.

The code for this would look something like this::

    from ievv_opensource.ievv_batchframework.models import BatchOperation

    myblogpost = Blog.objects.get(...)
    BatchOperation.objects.create_asyncronous(
        context_object_id=myblogpost,
        operationtype='new-blogpost-email')
    # code to send the batch operation to the batching service (like celery)
    # with a 15 minute delay, or just a service that polls for
    # BatchOperation.objects.filter(operationtype='new-blogpost-email',
    #                               started_datetime__lt=timezone.now() - timedelta(minutes=15))


    # The batching service code
    def my_batching_service(...):
        batchoperation = BatchOperation.objects.get(...)
        batchoperation.status = BatchOperation.STATUS_RUNNING
        batchoperation.save()
        # ... send out the emails ...
        batchoperation.finish()


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
    :members:
