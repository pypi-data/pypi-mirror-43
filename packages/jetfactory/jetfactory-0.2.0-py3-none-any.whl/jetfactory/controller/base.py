# -*- coding: utf-8 -*-

from jetfactory.registry import route_registry
from jetfactory.core.component import ComponentBase


class ControllerBase(ComponentBase):
    """Controller base class"""

    @classmethod
    def register(cls, pkg):
        """Makes the package available to this controller.

        :param pkg: jetfactory.Jetpack
        """

        cls._pkg_bind(pkg)

    async def on_ready(self):
        """Called upon initialization"""

    async def on_request(self, *args):
        """Called upon request arrival"""

    @property
    def registry(self):
        """Route registry iterator

        Iterates over RouteStacks, takes the stack.name (which corresponds to the handler function name)
        and returns reference to its instance method, along with the stack itself (schemas, paths, methods etc).

        :return: (<handler name>, <stack>)
        """

        for stack in route_registry.stacks.values():
            yield getattr(self, stack.name), stack

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
