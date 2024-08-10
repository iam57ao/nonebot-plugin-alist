from nonebot.adapters import Event
from nonebot_plugin_alconna import AlconnaMatcher, At

from .api import me
from .common import logout_and_switch_main_account
from .context import AlistUser, AlistUserManager
from .message import account_info_msg


async def get_alist_user(matcher: AlconnaMatcher, event: Event) -> AlistUser:
    user_id = event.get_user_id()
    alist_user = await AlistUserManager.get_by_user_id(user_id)
    if not alist_user:
        await matcher.finish(
            At("user", user_id) +
            "【Alist】您未登录任何账号!"
        )
    resp_body = await me(alist_user)
    if resp_body["code"] == 401:
        await matcher.send(
            At("user", user_id) +
            "【Alist】登录失效!"
        )
        main_account = await logout_and_switch_main_account(alist_user)
        if main_account:
            await matcher.finish(
                At("user", user_id) +
                "【Alist】您已切换到账户:\n" +
                account_info_msg(main_account)
            )
        else:
            await matcher.finish(
                At("user", user_id) +
                "【Alist】您未登录任何账号!"
            )

    return alist_user
