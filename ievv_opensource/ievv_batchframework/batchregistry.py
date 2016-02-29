import logging
from collections import OrderedDict

from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.module_loading import import_string

from ievv_opensource.utils.singleton import Singleton


# def make_action(actionclass, name='UnnamedAction'):
#     return type(name, (actionclass,))


class Action(object):
    @classmethod
    def run(cls, kwargs, executed_by_celery):
        action = cls(kwargs=kwargs, executed_by_celery=executed_by_celery)
        action.execute()

    def __init__(self, kwargs, executed_by_celery=False):
        self.kwargs = kwargs
        self.executed_by_celery = executed_by_celery
        # self.logger = kwargs['logger']

    @property
    def logger(self):
        logname = '{}.{}'.format(
            self.__class__.__module__,
            self.__class__.__name__)
        if self.executed_by_celery:
            return get_task_logger(logname)
        else:
            return logging.getLogger(logname)

    def execute(self):
        self.logger.info('HEI, %r', self.kwargs)


class ActionGroup(object):
    MODE_ASYNCRONOUS = 'asyncronous'
    MODE_SYNCRONOUS = 'syncronous'

    def __init__(self, name, actions=None, mode=None, route_to_alias=None):
        self.name = name
        self.mode = mode or self.MODE_ASYNCRONOUS
        self.route_to_alias = route_to_alias or Registry.ROUTE_TO_ALIAS_DEFAULT

        if self.mode == self.MODE_SYNCRONOUS and route_to_alias is None:
            raise ValueError('Can not specify a route_to_alias unless mode is {!r}'.format(
                self.MODE_ASYNCRONOUS))

        self.actions = []
        self.registry = None  # Set when the ActionGroup is added to the Registry
        if actions:
            self.add_actions(actions=actions)

    def add_action(self, action):
        self.actions.append(action)

    def add_actions(self, actions):
        for action in actions:
            self.add_action(action=action)

    def get_mode(self, **kwargs):
        return self.mode

    def run_syncronous(self, kwargs, executed_by_celery=False):
        for action in self.actions:
            action.run(kwargs=kwargs, executed_by_celery=executed_by_celery)

    def __get_route_to_callable(self):
        return self.registry.route_to_map[self.route_to_alias]

    def run_asyncronous(self, kwargs):
        # celery_tasks.default.delay(actiongroup_name=self.name)
        full_kwargs = {
            'actiongroup_name': self.name
        }
        full_kwargs.update(kwargs)
        # batchoperation = BatchOperation.objects.create_asyncronous(....)
        # full_kwargs['batchoperation_id'] = batchoperation.id
        celeryapp = Registry.get_instance()._celery_app
        celeryapp.send_task(
            name=self.__get_route_to_callable(),
            actiongroup_name=self.name,
            kwargs=full_kwargs)

    def run(self, **kwargs):
        mode = self.get_mode(**kwargs)
        if mode == self.MODE_ASYNCRONOUS:
            self.run_asyncronous(kwargs=kwargs)
        else:
            self.run_syncronous(kwargs=kwargs)


class Registry(Singleton):
    ROUTE_TO_ALIAS_DEFAULT = 'default'
    ROUTE_TO_ALIAS_HIGHPRIORITY = 'highpriority'

    def __init__(self):
        self.actiongroups = OrderedDict()
        self.route_to_map = {}
        self.__celery_app = None
        self.add_default_route_to_receivers()
        super(Registry, self).__init__()

    def add_default_route_to_receivers(self):
        self.add_route_to_alias(
            route_to_alias=self.ROUTE_TO_ALIAS_DEFAULT,
            route_to_callable='ievv_opensource.ievv_batchframework.celery_tasks.default',
        )
        self.add_route_to_alias(
            route_to_alias=self.ROUTE_TO_ALIAS_HIGHPRIORITY,
            route_to_callable='ievv_opensource.ievv_batchframework.celery_tasks.highpriority',
        )

    def add_route_to_alias(self, route_to_alias, route_to_callable):
        self.route_to_map[route_to_alias] = route_to_callable

    def add_actiongroup(self, actiongroup):
        actiongroup.registry = self
        self.actiongroups[actiongroup.name] = actiongroup

    def get_actiongroup(self, actiongroup_name):
        return self.actiongroups[actiongroup_name]

    def run(self, actiongroup_name, **kwargs):
        self.get_actiongroup(actiongroup_name=actiongroup_name).run(**kwargs)

    @property
    def _celery_app(self):
        if self.__celery_app is None:
            self.__celery_app = import_string(settings.IEVV_BATCHFRAMEWORK_CELERY_APP)
        return self.__celery_app
