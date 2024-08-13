import hashlib

from ...api.auth import login_hash
from ...exception.auth_exception import AuthException


async def login(site_url: str, username: str, password: str) -> str:
    password_hash = hashlib.sha256(
        f"{password}-https://github.com/alist-org/alist".encode()
    ).hexdigest()
    resp_body = await login_hash(site_url, username, password_hash)

    if resp_body["code"] != 200:
        message = resp_body["message"]
        raise AuthException(message)

    return resp_body["data"]["token"]
