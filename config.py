import json

Config = {
    'credentials': {
        'username': '',
        'token': ''
    },
    'ssh-key-path': None
}

try:
    with open('.config.json') as conf:
        Config = json.load(conf)
except FileNotFoundError:
    # just using default config above
    # TODO: add logging
    pass
