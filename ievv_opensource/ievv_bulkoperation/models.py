from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BulkOperation(models.Model):
    """
    Defines a bulk operation.

    This solves two challenges:

    1. A way to keep track of asyncronous operations. Typically used when you
       need to send a task to Celery or some other background/batch processing
       service, or even to a cronjob.
    2. When you need to do bulk create with multiple models.
       Lets say you have Game objects with a one-to-many relationship to Player
       objects with a one-to-many relationship to Card objects. You want to start all
       players in a game with a card. How to you bulk create all the players with a single card?
       You can easily bulk create players with ``bulk_create``, but you can not
       bulk create the cards because they require a Player. So you need to a way
       of retrieving the players you just bulk created. If you create a BulkOperation
       with :obj:`~.BulkOperation.context_object` set to the Game, you will get a unique
       identifier for the operation (the id of the BulkOperation). Then you can set
       that identifier as an attribute on all the bulk-created Player objects (preferrably
       as a foreign-key), and retrieve the bulk created objects by filtering on the
       id of the BulkOperation. After this, you can iterate through all the created
       Player objects, and create a list of Card objects for your bulk create operation
       for the cards.
    """

    #: One of the possible values for :obj:`~.BulkOperation.status`.
    #: Defines the BulkOperation as uprocessed (not yet started).
    #: This only makes sense for background tasks. They will typically
    #: be created with the unprocessed status, and then set to
    #: :obj:`~.BulkOperation.STATUS_RUNNING` when the batching service
    #: starts running the operation.
    STATUS_UNPROCESSED = 'unprocessed'

    #: One of the possible values for :obj:`~.BulkOperation.status`.
    #: Defines the BulkOperation as running (in progress).
    STATUS_RUNNING = 'running'

    #: One of the possible values for :obj:`~.BulkOperation.status`.
    #: Defines the BulkOperation as finished.
    STATUS_FINISHED = 'finished'

    #: Allowed values for :obj:`~.BulkOperation.status`.
    #: Possible values are:
    #:
    #: - :obj:`~.BulkOperation.STATUS_UNPROCESSED`.
    #: - :obj:`~.BulkOperation.STATUS_RUNNING`.
    #: - :obj:`~.BulkOperation.STATUS_FINISHED`.
    STATUS_CHOICES = [
        (STATUS_UNPROCESSED, 'unprocessed'),
        (STATUS_RUNNING, 'running'),
        (STATUS_FINISHED, 'finished'),
    ]

    #: One of the possible values for :obj:`~.BulkOperation.result`.
    #: This is used when we have no result yet (the operation is not finished).
    RESULT_NOT_AVAILABLE = 'not-available'

    #: One of the possible values for :obj:`~.BulkOperation.result`.
    #: Defines the BulkOperation as failed. This is set if the operation
    #: could not be completed because of an error. Any details about the
    #: result of the operation can be stored in :obj:`~.BulkOperation.output_data`.
    RESULT_SUCCESSFUL = 'successful'

    #: One of the possible values for :obj:`~.BulkOperation.result`.
    #: Defines the BulkOperation as failed. This is set if the operation
    #: could not be completed because of an error. Any error message(s)
    #: should be stored in :obj:`~.BulkOperation.output_data`.
    RESULT_FAILED = 'failed'

    #: Allowed values for :obj:`~.BulkOperation.result`.
    #: Possible values are:
    #:
    #: - :obj:`~.BulkOperation.RESULT_NOT_AVAILABLE`.
    #: - :obj:`~.BulkOperation.RESULT_SUCCESSFUL`.
    #: - :obj:`~.BulkOperation.RESULT_FAILED`.
    RESULT_CHOICES = [
        (RESULT_NOT_AVAILABLE, 'not available yet (processing not finished)'),
        (RESULT_SUCCESSFUL, 'successful'),
        (RESULT_FAILED, 'failed'),
    ]

    #: The user that started this bulk operation.
    #: Optional, but it is good metadata to add for debugging.
    started_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        null=True)

    #: The datetime when this bulk operation was started.
    #: Defaults to ``timezone.now()``.
    started_datetime = models.DateTimeField(
        default=timezone.now)

    # #: Is this an asyncronous operation? Set this to ``True`` for
    # #: background tasks (such as Celery tasks).
    # asyncronous = models.BooleanField(
    #     default=False)

    #: The content type for :obj:`~.BulkOperation.context_object`.
    context_content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        null=True)

    #: The id field for :obj:`~.BulkOperation.context_object`.
    context_object_id = models.PositiveIntegerField(
        null=True)

    #: Generic foreign key that identifies the context this operation
    #: runs in. This is optional.
    context_object = GenericForeignKey('context_content_type', 'context_object_id')

    #: The type of operation. This is application specific - you
    #: typically use this if you allow multiple different bulk operations
    #: on the same :obj:`~BulkOperation.context_object`.
    #: This is not required, and defaults to empty string.
    operationtype = models.CharField(
        max_length=255, db_index=True,
        null=False, blank=True, default='')

    #: The status of the operation.
    #: The allowed values for this field is documented in
    #: :obj:`~.BulkOperation.STATUS_CHOICES`.
    #: Defaults to :obj:`~.BulkOperation.STATUS_UNPROCESSED`.
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_UNPROCESSED)

    #: The result of the operation.
    #: The allowed values for this field is documented in
    #: :obj:`~.BulkOperation.RESULT_CHOICES`.
    #: Defaults to :obj:`~.BulkOperation.RESULT_NOT_AVAILABLE`.
    result = models.CharField(
        max_length=12,
        choices=RESULT_CHOICES,
        default=RESULT_NOT_AVAILABLE)

    #: Input data for the BulkOperation.
    input_data = models.TextField(
        null=False, blank=True, default='')

    #: Output data for the BulkOperation.
    output_data = models.TextField(
        null=False, blank=True, default='')

    def clean(self):
        if self.status == self.STATUS_FINISHED and self.result == self.RESULT_NOT_AVAILABLE:
            raise ValidationError({
                'result': 'Must be "successful" or "failed" when status is "finished".'
            })
