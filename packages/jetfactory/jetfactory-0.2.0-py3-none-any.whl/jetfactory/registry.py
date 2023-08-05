# -*- coding: utf-8 -*-


class RouteStack:
    hid = None  # handler ID
    handler = None
    name = None
    path = None
    method = None
    schemas = {}

    def __dict__(self):
        return self.__class__.__dict__

    def add_route(self, handler, path, method):
        self.handler = handler
        self.name = handler.__name__
        self.path = path
        self.method = method


class RouteRegistry:
    stacks = {}

    def __getitem__(self, hid):
        if hid not in self.stacks:
            self.stacks[hid] = RouteStack()

        return self.stacks[hid]


def get_handler_id(handler):
    hid = hash(handler.__module__ + handler.__name__)
    return route_registry[hid]


route_registry = RouteRegistry()
