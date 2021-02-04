from flask import Flask, request, Response
from git_cli.gkm import GitCLIClient

from config import Config
from github_api_client.github import GitHubOrgAPIClient

app = Flask(__name__)

URL_PREFIX = '/api/v1'

config = Config()


@app.route(URL_PREFIX + '/clone/')
def create_clone():
    if request.method != 'POST':
        return Response("Method not allowed", status=405)
    data = request.json
    origin_repository = data['origin']
    repository_name = ''  # TODO: fill the repo's name
    org_name = ''  # TODO: fill the org's name
    with GitCLIClient(config.get('ssh-key-path'), '/tmp') as git_cli:
        git_cli.clone(origin_repository)
        gh_client = GitHubOrgAPIClient(org_name, config.get('credentials'))
        response = gh_client.create_repository(name=repository_name)
        ssh_url = response.json()['ssh_url']
        git_cli.push(ssh_url, 'main')
