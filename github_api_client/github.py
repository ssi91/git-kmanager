import base64

import requests


class MethodNotImplementedError(Exception):
    pass


class GitHubOrgAPIClient:
    BASE_URL = 'https://api.github.com'
    api_url_pattern = '/orgs/{org}/{resource}'

    def __init__(self, org_name, credentials):
        self._org_name = org_name
        self.__credential = credentials

    def _authorization_header(self, auth_type='basic'):
        if auth_type == 'basic':
            return base64.b64encode(
                f'{self.__credential["username"]}:{self.__credential["token"]}'.encode('ascii')
            ).decode('ascii')

    def _request(self, method, url, query_params=None, json_params=None):
        methods = {
            'get': (
                requests.get,
                {
                    'url': url,
                    'params': query_params
                }
            ),
            'post': (
                requests.post,
                {
                    'url': url,
                    'json': json_params
                }
            )
        }

        try:
            response = methods[method][0](**methods[method][1],
                                          headers={'Authorization': f'Basic {self._authorization_header()}'})
        except KeyError as key:
            raise MethodNotImplementedError("Method %s is not implemented yet" % key)

        response_data = response.json()

        return response_data

    def get_repositories(self, **kwargs):
        return self._request(
            'get',
            f'{self.BASE_URL}{self.api_url_pattern.format(org=self._org_name, resource="repos")}',
            query_params=kwargs
        )

    def create_repository(self, **kwargs):
        return self._request(
            'post',
            f'{self.BASE_URL}{self.api_url_pattern.format(org=self._org_name, resource="repos")}',
            json_params=kwargs
        )


class GitHubAPIClient:
    BASE_URL = 'https://api.github.com'

    def __init__(self, repo_provider, credentials):
        self._repo_provider = repo_provider

    def get_repositories(self, **kwargs):
        return self._repo_provider.get_repositories(self.BASE_URL, **kwargs)
