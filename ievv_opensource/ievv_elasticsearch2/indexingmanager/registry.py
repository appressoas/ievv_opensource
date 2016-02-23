from collections import OrderedDict

from django.utils.module_loading import import_string

from ievv_opensource.utils.singleton import Singleton


class AbstractExecute(object):
    def __init__(self, action, **kwargs):
        self.action = action

    def run(self):
        raise NotImplementedError()


class BlockingExecute(AbstractExecute):
    def run(self):
        pass  # Run in realtime


class BackgroundExecute(AbstractExecute):
    def delay_milliseconds(self, batchoperation):
        """
        Number of milliseconds until we can start the worker.

        Defaults to ``0``, which means start the operation at once.

        This is ignored unless ``mode`` is :obj:`.MODE_BACKGROUND`.

        If this returns a number larger than ``0``,

        You can override this to perform checks that avoid multiple
        overlapping indexing updates starting at the same time.

        Args:
            batchoperation: The :class:`ievv_opensource.ievv_batchframework.models.BatchOperation`
                that we are trying to start.
        """
        return 0

    def run(self):
        pass  # Run in celery, or delay_milliseconds


class Action(object):
    #: The value to use as the ``mode`` parameter if you want
    #: the action to be performed in realtime/blocking mode.
    MODE_BLOCKING = 'blocking'

    #: The value to use as the ``mode`` parameter if you want
    #: the action to be performed in background mode.
    MODE_BACKGROUND = 'background'

    #: The value to use as the ``worker`` parameter you want
    #: the action to run in the default worker.
    WORKER_DEFAULT = 'default'

    #: The value to use as the ``worker`` parameter you want
    #: the action to run in the high-priority worker.
    WORKER_HIGHPRIORITY = 'highpriority'

    def __init__(self, action, mode=MODE_BLOCKING, worker=WORKER_DEFAULT):
        self.action = action
        self.mode = mode
        self.worker = worker

    @property
    def worker_method(self):
        pass  # import_string() - translate the default workers to pythonpath

    def get_execute_class(self):
        return BackgroundExecute

    def execute(self, **kwargs):
        execute_class = self.get_execute_class()
        execute_class(action=self, **kwargs).run()


class ActionSet(object):
    def __init__(self, signalpath, actions=None):
        self.signalpath = signalpath
        self.actions = []
        if actions:
            self.add_actions(*actions)
        self.doctype_class = None

    def add_actions(self, *actions):
        for action in actions:
            self.actions.append(action)


class SignalSet(object):
    def __init__(self, doctype_class_path, actionsets=None):
        self.doctype_class_path = doctype_class_path
        self.actionsets = []
        if actionsets:
            self.add_actionsets(actionsets)

    @property
    def doctype_class(self):
        return import_string(self.doctype_class_path)

    def add_actionsets(self, *actionsets):
        for actionset in actionsets:
            self.actionsets.append(actionset)


class Registry(Singleton):
    def __init__(self):
        self.indexing_doctypes = OrderedDict()
        super(Registry, self).__init__()

    def add_signalset(self, signalset):
        self.indexing_doctypes[signalset.doctype_class_path] = signalset
