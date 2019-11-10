import os.path
import json
def _get_local_path(filepath):
    """Convert the filepath uri to an absolute path in the FS."""
    return os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])

def load_config(config = {}, filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath) as file:
        j = json.loads(file.read())
        config.update(j)
        
_config = {
        'lockserver': None,
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
        }
load_config(_config, 'fileserver.dfs.json')

def get_configs():
    return _config


def get_host_port(s):
    """Return a tuple ('host', port) from the string s.
       e.g.: 'localhost:80' → ('localhost', 80)
    """

    host, port = s.split(':')
    return host, int(port)
