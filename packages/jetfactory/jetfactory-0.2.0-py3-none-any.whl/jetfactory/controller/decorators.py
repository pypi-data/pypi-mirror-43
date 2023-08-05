# -*- coding: utf-8 -*-

from enum import Enum
from functools import wraps

import ujson
from sanic.request import Request
from sanic.response import HTTPResponse

from jetfactory.registry import get_handler_id


class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'


def _schema_prepare(schema_cls):
    """Makes schema ready for use with Jetfactory

    1) Takes a schema class
    2) Creates `Meta` subclass if not set
    3) Sets `ujson` render_module

    :param schema_cls: Marshmallow.Schema class
    :return: instance of `schema_cls`
    """

    if not hasattr(schema_cls, 'Meta'):
        meta = type('Meta', (type,), {})
        schema_cls.Meta = meta

    schema_cls.Meta.render_module = ujson
    return schema_cls()


def output_dump(schema_cls, status=200, many=False):
    """Returns a transformed and serialized HTTPResponse

    :param schema_cls: Marshmallow.Schema class
    :param status: Return status (on success)
    :param many: Whether to return a list or single object
    :return: HTTPResponse
    """

    schema = _schema_prepare(schema_cls)

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            args_new = list(args)

            # Remove `Request` object from args (in case it wasn't consumed by `input_local`).
            if len(args) > 1 and isinstance(args[1], Request):
                args_new.pop(1)

            rv = await fn(*args_new, **kwargs)

            # Return HTTP encoded JSON response
            return HTTPResponse(
                body=schema.dumps(rv, indent=4, many=many),
                status=status,
                content_type='application/json'
            )

        r = get_handler_id(handler)

        # Add the `response` schema to this route handler's stack
        r.schemas.update({'response': schema})

        return handler

    return wrapper


def input_load(**schemas):
    """Takes a list of schemas used to validate and transform parts of a request object.
    The selected parts are injected into the route handler as arguments.

    :param schemas: list of schemas (kwargs)
    :return: Route handler
    """

    schemas = {k: _schema_prepare(v) for k, v in schemas.items()}

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            args_new = list(args)

            request = kwargs['request'] if 'request' in kwargs else args_new.pop(1)

            if 'body' in schemas:
                kwargs.update({'body': schemas['body'].load(request.json)})

            if 'query' in schemas:
                kwargs.update({'query': schemas['query'].load(request.args)})

            return await fn(*args_new, **kwargs)

        r = get_handler_id(handler)

        # Add the provided schemas to the RouteStack
        r.schemas.update(schemas)

        return handler

    return wrapper


def route(path, method, inject=None):
    """Prepares route registration, and performs handler injection.

    :param path: Handler path, relative to application and package paths
    :param method: HTTP Method
    :param inject: List of `Injector` injections
    :return: Route handler
    """

    injections = inject or []

    if isinstance(method, str):
        method = Method(method.upper()).value

    def wrapper(fn):
        @wraps(fn)
        async def handler(*inner_args, **inner_kwargs):
            request = inner_args[1]
            args_new = list(inner_args)

            # Handle injections and inject as kwargs.
            for injection in injections:
                if callable(injection.value):
                    func = injection.value
                    value = func(request)
                elif injection.name == 'request':
                    # Full request injection, remove duplicate.
                    value = args_new.pop(1)
                else:
                    raise Exception('Unknown injection')

                inner_kwargs.update({injection.name: value})

            return await fn(*args_new, **inner_kwargs)

        r = get_handler_id(handler)

        # Adds the handler for registration once the loop is ready.
        r.add_route(handler, path, method)

        return handler

    return wrapper
