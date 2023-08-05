from meos_sdk.app import MeosApp, Response, ResponseStatus


test_app = MeosApp('test_app')


@test_app.rpc_entry_point()
def test(*, msg):
    return Response(
        status=ResponseStatus.Ok,
        data={'msg': msg}
    )
