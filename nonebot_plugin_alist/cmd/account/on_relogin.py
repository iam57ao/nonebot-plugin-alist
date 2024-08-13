from typing import Annotated

from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.params import EventPlainText
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

from ...common.auth_service.login_service import login
from ...context.alist_user import AlistUserManager
from ...exception.auth_exception import AuthException
from ...message.account import account_info_msg, account_list_msg
from ...models import AlistAccount, User
from ..alist_commands import alist_cmd

relogin_cmd = alist_cmd.dispatch("relogin")


@relogin_cmd.handle()
async def handle_group_message(event: GroupMessageEvent):
    await relogin_cmd.finish(
        At("user", event.get_user_id()) + "【Alist】请私聊重新登录!"
    )


@relogin_cmd.handle()
async def _(event: Event, state: T_State):
    user_id = event.get_user_id()
    user_account = await User.get_or_none(user_id=user_id)
    if not user_account:
        await relogin_cmd.finish("【Alist】您没有需要重新登录的账户!")
    await user_account.fetch_related("alist_accounts")
    alist_accounts = user_account.alist_accounts
    if not alist_accounts:
        await relogin_cmd.finish("【Alist】您没有需要重新登录的账户!")
    else:
        state.update(
            {
                "user_id": user_id,
                "user_account": user_account,
                "alist_accounts": alist_accounts,
            }
        )
        await relogin_cmd.pause(
            "【Alist】请回复要重新登录的账户序号:\n" + account_list_msg(alist_accounts)
        )


@relogin_cmd.handle()
async def _(index: Annotated[str, EventPlainText()], state: T_State):
    if not index.isdigit():
        await relogin_cmd.finish("【Alist】输入不合法!")
    alist_accounts = state["alist_accounts"]
    index = int(index)
    if index < 0 or index >= len(alist_accounts):
        await relogin_cmd.finish("【Alist】输入的序号范围不合法!")
    alist_account: AlistAccount = alist_accounts[index]
    state["alist_account"] = alist_account
    await relogin_cmd.pause(
        "【Alist】重新登录以下账户:\n"
        + account_info_msg(alist_account)
        + "\n请输入密码:"
    )


@relogin_cmd.handle()
async def _(password: Annotated[str, EventPlainText()], state: T_State):
    alist_account: AlistAccount = state["alist_account"]
    try:
        token = await login(
            alist_account.site_url, alist_account.site_username, password
        )
    except AuthException as e:
        await relogin_cmd.finish(f"【Alist】重新登录失败! 错误信息: {e.message}")
    else:
        alist_account.token = token
        await alist_account.save()
        user_account: User = state["user_account"]
        user_id = state["user_id"]
        await user_account.set_main_account(alist_account)
        AlistUserManager.remove_by_user_id(user_id)
        await relogin_cmd.send("【Alist】重新登录成功!")
        await relogin_cmd.finish(
            At("user", user_id)
            + "【Alist】您已切换到账户:\n"
            + account_info_msg(alist_account)
        )
