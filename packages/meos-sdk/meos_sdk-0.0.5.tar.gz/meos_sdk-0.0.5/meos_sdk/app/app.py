import inspect
from functools import wraps, partial
import typing as t
from urllib import parse

from flask import Flask, request, Blueprint
from flask.helpers import send_from_directory
import yaml

from .response import Response, ResponseStatus
from .config import setup_yaml_parser
from .exceptions import MeosAppException


def _should_inject_param(param, *, func):
    arg_spec = inspect.getfullargspec(func)
    return arg_spec.varkw or param in arg_spec.kwonlyargs


def _inject_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if _should_inject_param('request', func=fn):
            return fn(*args, request=request, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper


def _inject_config(app):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if _should_inject_param('config', func=fn):
                return fn(*args, config=dict(app.config), **kwargs)
            else:
                fn(*args, **kwargs)
        return wrapper
    return decorator


def _inject_params(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **(request.json or {}), **kwargs)
    return wrapper


def _map_meos_response_flask_response(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            response: Response = fn(*args, **kwargs)
        except MeosAppException as exc:
            response = Response(
                status=ResponseStatus.GenericError,
                data={'error_key': exc.key}
            )
        return response.flask_response()
    return wrapper


class EntryPoint():
    def __init__(
            self, route, *, methods=['GET'],
            defaults=None):
        self.route = route
        self.methods = methods
        self.defaults = defaults


class MeosApp(Flask):

    def __init__(self, *args, config_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_config(config_path)
        self.after_request(self.add_cors_headers)

    def add_cors_headers(self, response):
        response.headers[
            'Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        origin = request.headers.get('Origin')
        if origin:
            parsed_url = parse.urlparse(origin)
            if parsed_url.netloc.endswith(self.config.get('MEOS_DOMAIN')):
                response.headers[
                    'Access-Control-Allow-Origin'] = (
                        f"https://{parsed_url.netloc}")
                response.headers['Access-Control-Allow-Credentials'] = 'true'
        # Required for Webpack dev application to make  requests to flask api
        # from another host (localhost:8080)
        if self.config.get('ALLOW_ALL_CORS'):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers["Access-Control-Allow-Methods"] = (
                "GET,POST,HEAD,OPTIONS,PUT,DELETE,PATCH")
        return response

    def load_config(self, config_path):
        setup_yaml_parser()
        if config_path:
            with open(config_path) as f:
                self.config = {**self.config, **yaml.load(f)}

    def merge_app(self, app):
        blue_print = Blueprint(
            app.name,
            app.import_name,
            static_folder=app.static_folder,
            static_url_path=app.static_url_path)
        self.register_blueprint(blue_print)

    def rpc_entry_point(self):
        def decorator(fn):
            route = f'/{fn.__name__}'
            decorators = [
                _inject_config(self),
                _inject_params,
                _map_meos_response_flask_response,
                self.route(route, methods=['POST']),
            ]
            wrapped_func = fn
            for decorator in decorators:
                wrapped_func = decorator(wrapped_func)
            # wrapped_func = self.route(route, methods=['POST'])(
            #     _map_meos_response_flask_response(
            #         _inject_params(fn)
            #     )
            # )

            @wraps(fn)
            def wrapper(*args, **kwargs):
                return wrapped_func(*args, *kwargs)
            return wrapper
        return decorator

    def http_entry_point(self, route, *,
                         methods=['GET'], defaults=None
                         ) -> t.Callable:
        def decorator(fn):
            wrapped_func = self.route(
                    route, methods=methods,
                    defaults=defaults)(
                _map_meos_response_flask_response(
                    _inject_request(fn)
                )
            )

            @wraps(fn)
            def wrapper(*args, **kwargs):
                return wrapped_func(*args, *kwargs)
            return wrapper
        return decorator

    def http_entry_points(self, entrypoints) -> t.Callable:
        def decorator(fn):
            _func = _inject_request(fn)
            _func = _map_meos_response_flask_response(
                _func)
            for entrypoint in entrypoints:
                _func = self.route(
                    entrypoint.route, methods=entrypoint.methods,
                    defaults=entrypoint.defaults
                )(_func)

            @wraps(fn)
            def wrapper(*args, **kwargs):
                return _func(*args, *kwargs)
            return wrapper
        return decorator

    def http_static_folder(self, *, url_path, dir_path):
        self.add_url_rule(
                url_path + '/<path:filename>',
                endpoint='static' + str(hash(url_path)),
                view_func=partial(send_from_directory, dir_path)
            )

    def update_config(self, config):
        self.config = {**self.config, **config}
        return self.config
