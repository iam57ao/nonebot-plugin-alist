from httpx import AsyncClient
from nonebot import get_plugin_config

from .config import Config
from .context.alist_user import AlistUser

plugin_config = get_plugin_config(Config)


def async_client(site_url: str) -> AsyncClient:
    return AsyncClient(base_url=site_url, timeout=plugin_config.alist_request_timeout)


async def authenticated_client(alist_user: AlistUser) -> AsyncClient:
    user_account = alist_user.user_account
    account = await user_account.get_main_account()
    token = account.token if account else ""
    return AsyncClient(
        base_url=account.site_url,
        headers={"Authorization": token},
        timeout=plugin_config.alist_request_timeout,
    )
