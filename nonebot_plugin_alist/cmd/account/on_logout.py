from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends, EventPlainText
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

from ...common.auth_service.logout_service import logout_and_switch_main_account
from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...message.account import account_info_msg
from ..alist_commands import alist_cmd

logout_cmd = alist_cmd.dispatch("logout")


@logout_cmd.handle()
async def _(
    event: Event,
    alist_user: Annotated[AlistUser, Depends(get_alist_user)],
    state: T_State,
):
    main_account = await alist_user.user_account.get_main_account()
    site_url = main_account.site_url
    username = main_account.site_username
    user_id = event.get_user_id()
    state.update({"alist_user": alist_user, "user_id": user_id})
    await logout_cmd.pause(
        At("user", user_id) + f"【Alist】登出确认:\n"
        f"网站为 {site_url}\n"
        f"用户名为 {username}\n"
        f"是否确定？(请回复 是/否)"
    )


@logout_cmd.handle()
async def _(confirm: Annotated[str, EventPlainText()], state: T_State):
    user_id = state["user_id"]
    if confirm == "是":
        alist_user: AlistUser = state["alist_user"]
        main_account = await logout_and_switch_main_account(alist_user)
        await logout_cmd.send(At("user", user_id) + "【Alist】您已成功登出!")
        if not main_account:
            await logout_cmd.finish(At("user", user_id) + "【Alist】您已登出所有账户!")
        else:
            await logout_cmd.finish(
                At("user", user_id)
                + "【Alist】您已切换到账户:\n"
                + account_info_msg(main_account)
            )
    else:
        await logout_cmd.finish(At("user", user_id) + "【Alist】操作取消!")
