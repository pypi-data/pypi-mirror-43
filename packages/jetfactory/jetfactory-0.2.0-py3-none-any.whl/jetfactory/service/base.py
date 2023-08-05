# -*- coding: utf-8 -*-

from uvloop.loop import Loop

from jetfactory import Application
from jetfactory.core.component import ComponentBase


class BaseService(ComponentBase):
    """The Service base class used for creating Package Services, it implements the
    singleton pattern as Services are commonly used in many parts of a Package.

    :ivar app: Jetfactory application instance
    :ivar loop: Asyncio event loop (uvloop)
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(BaseService, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    app: Application
    loop: Loop

    @classmethod
    def register(cls, pkg, mgr):
        """Class method used internally by the Jetfactory manager to register a Service

        :param pkg: instance of :class:`jetfactory.Jetpack`
        :param mgr: instance of :class:`Jetfactory.JetManager`
        """

        cls.loop = mgr.loop
        cls.app = mgr.sanic
        cls._pkg_bind(pkg)
