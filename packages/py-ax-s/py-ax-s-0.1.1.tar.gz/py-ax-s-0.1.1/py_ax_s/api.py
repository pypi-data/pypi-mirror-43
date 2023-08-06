"""
py_ax_s.api
~~~~~~~~~~~

This module implements the ax-s API interface.

:copyright: (c) 2019 by Elliott Maguire
"""

import requests


class API:
    """ Enables interaction with the ax-s API.

    :param token: a user's platform access token
    """
    def __init__(self, key):
        self.key = key

    def call(self, token, name, **kwargs):
        """ Calls a given endpoint.

        :param token: a registered API's access token
        :param name: a registered endpoint's name
        """
        url = f"https://easy.ax-s.io/api/call/{token}?endpoint={name}"
        headers = {'Authorization': f"Token {self.key}"}
        body = {}
        for k, v in kwargs.items():
            if k in ('headers', 'params', 'body'):
                body[k] = v

        response = requests.post(url, headers=headers, data=body)

        return response

