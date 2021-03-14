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
    return origin[origin.rfind('/') + 1:origin.rfind('.')]


@app.route(URL_PREFIX + '/clone/', methods=('POST',))
def create_clone():
    data = request.json
    origin_repository = data['origin']
    repository_name = data.get('repository') or _repo_form_origin(origin_repository)
    org_name = data.get('org_name', config.get('org_name'))
    with GitCLIClient(config.get('ssh-key-path'), clone_path) as git_cli:
        clone_response = git_cli.clone(origin_repository)
        if not clone_response['success']:
            # TODO: add logging
            # TODO implement git pull
            pass
        gh_client = GitHubOrgAPIClient(org_name, config.get('credentials'))
        status_code, response = gh_client.create_repository(name=repository_name)
        status = None
        if status_code == 201:
            status = 'Created'
        if status_code == 422:
            status_code, response = gh_client.get_repository(repository_name)
            status = 'Updated'
        ssh_url = response['ssh_url']
        os.chdir(f'{clone_path}/{repository_name}')
        branch_response = git_cli.branch()
        main_branch = branch_response['result'][0]  # TODO: check the status
        git_cli.push(ssh_url, main_branch)

    return {
        'status': status,
        'repository': {},
        'msg': ''
    }
