
import json

from flask import make_response


class _Status:
    http_status_map = {
        'ok': 200,
        'generic_error': 422
    }

    def __init__(self, status):
        self.status = status

    @property
    def http(self):
        return self.http_status_map[self.status]

    def __repr__(self):
        return self.status


class ResponseStatus:
    Ok: _Status = _Status('ok')
    GenericError: _Status = _Status('generic_error')


class Response:

    def __init__(
            self, *, status: _Status=ResponseStatus.Ok, data: dict=None,
            file=None, content: str=None):
        self.status = status
        self.data = data
        self.content = content
        if file:
            with open(file) as f:
                self.content = f.read()
        if self.content and self.data:
            raise ValueError(
                'Either \'data\' or \'content\' should'
                ' be passed but not both ')

    def flask_response(self):
        flask_response = make_response(
            self.content or json.dumps(self.data),
            self.status.http,
        )
        if self.data:
            flask_response.mimetype = "application/json"
        return flask_response

    def error_response(self, *, error_key):
        body = {
            'error_key': error_key
        }
        flask_response = make_response(
            json.dumps(body),
            400,
        )
        flask_response.mimetype = "application/json"
        return flask_response
