from app import _repo_form_origin


def test__repo_from_origin():
    inp = 'git@github.com:ssi91/git-kmanager.git'

    assert 'git-kmanager' == _repo_form_origin(inp)
