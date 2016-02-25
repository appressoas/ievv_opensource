from collections import OrderedDict

from ievv_opensource.ievv_batchframework import celery_tasks
from ievv_opensource.utils.singleton import Singleton

from ievv_opensource.demo.project.celery import app as celeryapp


class Action(object):
    def __init__(self, name='unnamed action'):
        self.name = name

    def run(self, **kwargs):
        print()
        print("*" * 70)
        print()
        print(kwargs)
        print()
        print("*" * 70)
        print()


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

    def run_syncronous(self, **kwargs):
        for action in self.actions:
            action.run(**kwargs)

    def __get_route_to_callable(self):
        return self.registry.route_to_map[self.route_to_alias]

    def run_asyncronous(self, **kwargs):
        # celery_tasks.default.delay(actiongroup_name=self.name)
        full_kwargs = {
            'actiongroup_name': self.name
        }
        full_kwargs.update(kwargs)
        # batchoperation = BatchOperation.objects.create_asyncronous(....)
        # full_kwargs['batchoperation_id'] = batchoperation.id
        celeryapp.send_task(
            name=self.__get_route_to_callable(),
            actiongroup_name=self.name,
            kwargs=full_kwargs)

    def run(self, **kwargs):
        mode = self.get_mode(**kwargs)
        if mode == self.MODE_ASYNCRONOUS:
            self.run_asyncronous(**kwargs)
        else:
            self.run_syncronous(**kwargs)


class Registry(Singleton):
    ROUTE_TO_ALIAS_DEFAULT = 'default'
    ROUTE_TO_ALIAS_HIGHPRIORITY = 'highpriority'

    def __init__(self):
        self.actiongroups = OrderedDict()
        self.route_to_map = {}
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
