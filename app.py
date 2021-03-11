import os

from flask import Flask, request
from git_cli.gkm import GitCLIClient

from config import Config
from github_api_client.github import GitHubOrgAPIClient

app = Flask(__name__)

URL_PREFIX = '/api/v1'

config = Config

clone_path = os.environ.get('CLONE_PATH')


def _repo_form_origin(origin: str):
    # TODO: test that!
    return origin[origin.rfind('/'):origin.rfind('.')]


@app.route(URL_PREFIX + '/clone/', methods=('POST',))
def create_clone():
    data = request.json
    origin_repository = data['origin']
    repository_name = data['repository'] or _repo_form_origin(origin_repository)
    org_name = data.get('org_name', config.get('org_name'))
    with GitCLIClient(config.get('ssh-key-path'), clone_path) as git_cli:
        git_cli.clone(origin_repository)
        gh_client = GitHubOrgAPIClient(org_name, config.get('credentials'))
        response = gh_client.create_repository(name=repository_name)
        ssh_url = response['ssh_url']
        os.chdir(f'{clone_path}/{repository_name}')
        git_cli.push(ssh_url, 'master')  # TODO: use actual default branch

    return 'success'
