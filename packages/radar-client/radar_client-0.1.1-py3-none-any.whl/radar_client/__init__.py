import requests
from .utils import lscmp, sign


def create_query(name, requires=None, props=None):
    default_requires = requires
    default_props = props

    def init(requires=None, **props):
        return {
            'name': name,
            'requires': requires or default_requires,
            'props': props or default_props
        }

    return init


def radar(url, public_key=None, secret_key=None, header_name='x-radar-signature'):
    signature = None

    if public_key and secret_key:
        signature = sign(public_key, secret_key)

    def request(*queries, headers=None):
        headers = headers or {}

        if signature:
            headers = {**headers, header_name: signature}

        return requests.post(url, json=queries, headers=headers).json()

    return request
