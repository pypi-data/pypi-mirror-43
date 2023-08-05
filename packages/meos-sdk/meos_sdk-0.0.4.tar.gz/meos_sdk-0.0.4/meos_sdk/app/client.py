import requests


class MeosAppClient():

    def __init__(self):
        self.base_url = 'http://example.org'

    @staticmethod
    def api_call_wrapper(*, base_url, name):
        def api_call(*args, **kwargs):
            url = base_url.strip('/') + f'/{name}'
            return requests.post(url, json=kwargs)
        return api_call

    def __getattr__(self, name):
        return MeosAppClient.api_call_wrapper(
            base_url=self.base_url, name=name)
