from meos_sdk.testing.client import MeosAppTestClient
from meos_sdk.app import MeosApp, Response
from meos_sdk.app.app import _should_inject_param
from meos_sdk.app import MeosAppException


def test_app(test_app_client):
    # Given
    status = 200
    data = {'msg': 'hello'}

    # When
    res = test_app_client.test(**data)

    # Then
    assert res.status_code == status
    assert res.json == data


def test_rpc_entry_point():
    # Given
    app = MeosApp('test')
    config = {1: 1}
    app.update_config(config)

    def _func(*args, config, **kwargs):
        return Response(data=config[1])
    app.rpc_entry_point()(_func)
    test_client = MeosAppTestClient(app=app)

    # When
    res = test_client._func()

    # Then
    assert res.status_code == 200
    assert res.json == 1


def test_should_inject_param():
    # Given
    param = 'param'

    def _func_1():
        return None

    def _func_2(*, param):
        return None

    def _func_3(*args, **kwargs):
        return None

    # When
    should_inject_1 = _should_inject_param(param, func=_func_1)
    should_inject_2 = _should_inject_param(param, func=_func_2)
    should_inject_3 = _should_inject_param(param, func=_func_3)

    # Then
    assert not should_inject_1
    assert should_inject_2
    assert should_inject_3


def test_error_handling():
    # Given
    app = MeosApp('test')
    error_key = 'blah'

    def _func(*args, **kwargs):
        nonlocal error_key
        raise MeosAppException(key=error_key)
    app.rpc_entry_point()(_func)
    test_client = MeosAppTestClient(app=app)

    # When
    res = test_client._func()

    # Then
    assert res.status_code == 422
    assert res.json['error_key'] == error_key
