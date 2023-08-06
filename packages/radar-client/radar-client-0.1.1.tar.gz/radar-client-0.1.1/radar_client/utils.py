import hmac
from functools import wraps
from radar_server import QueryError
from base64 import b64encode, b64decode
from hashlib import sha256


def sign(public_key, secret_key):
    sig = hmac.new(key=secret_key.encode(), msg=public_key.encode(), digestmod=sha256).digest()
    return b64encode(sig).decode('utf8')


def verify_sig(msg, public_key, secret_key):
    sig = sign(public_key, secret_key)

    if sig is None:
        raise InvalidRadarSignature('Missing a Radar signature header')

    result = hmac.compare_digest(msg, sig)

    if result is False:
        raise InvalidRadarSignature('Invalid Radar signature')

    return result


class InvalidRadarSignature(QueryError):
    pass


def authorize(request, public_key, secret_key, header_name='x-radar-signature'):
    def verify_request(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            sig = request.headers.get(header_name)
            verify_sig(sig, public_key, secret_key)
            return fn(*a, **kw)

        return wrapper

    return verify_request

