import os, sys
import json
import urllib

server_url = 'https://aping-pong.herokuapp.com'

def call(path, id_code='', show_cmd=False, is_post=False, **kwargs):
    """Execute curl commands to access game API endpoints.

    Inputs
    ------
    path:      API endpoint leading slash [string]
    id_code:   Unique private id [string]
    show_cmd:  Print the full curl command executed to stdout [bool, default False]
    is_post:   Not currently used for this game, but controls how parameters are passed
    **kwargs:  Other keyword arguments to pass either as regular parameters (is_post=False) or
                 as form parameters (is_post=True)
    """
    params = []
    if id_code != '':
        params.append(('private_id', id_code))
    path = urllib.parse.quote(path)
    # silent mode for curl
    cmd = f'curl -s "{server_url}/{path}'
    if is_post:
        # add trailing double quote prior to form params
        cmd += '?' + urllib.parse.urlencode(params) + '"'
        for k, v in kwargs.items():
            cmd += f" --form {k}={v}"
    else:
        params.extend(list(kwargs.items()))
        cmd += '?' + urllib.parse.urlencode(params) + '"'
    if show_cmd:
        print(cmd)
    res = os.popen(cmd).read()
    try:
        return json.loads(res)
    except:
        return res

def declare_player(level, pID=None, show_cmd=False):
    if pID is None:
        info = call('request_game/{}'.format(level), show_cmd=show_cmd)
    else:
        info = call('request_game/{}'.format(level), id_code=pID, show_cmd=show_cmd)
    return info
