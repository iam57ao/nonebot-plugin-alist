from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import EventPlainText
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

from ...context.alist_user import AlistUserManager
from ...message.account import account_info_msg, account_list_msg
from ...models import User
from ..alist_commands import alist_cmd

account_switch_cmd = alist_cmd.dispatch("account.switch")


@account_switch_cmd.handle()
async def _(event: Event, state: T_State):
    user_id = event.get_user_id()
    user_account = await User.get_or_none(user_id=user_id)
    await user_account.fetch_related("alist_accounts")
    main_account = await user_account.get_main_account()
    alist_accounts = user_account.alist_accounts
    alist_accounts = [
        alist_account for alist_account in alist_accounts if alist_account.token
    ]
    if main_account in alist_accounts:
        alist_accounts.remove(main_account)
    if alist_accounts:
        state.update(
            {
                "user_id": user_id,
                "alist_accounts": alist_accounts,
                "user_account": user_account,
            }
        )
        await account_switch_cmd.pause(
            At("user", user_id)
            + "【Alist】请输入您要切换到账户的序号:\n"
            + account_list_msg(alist_accounts)
        )
    else:
        await account_switch_cmd.finish(
            At("user", user_id) + "【Alist】没有一个已经登录的账户可用于切换!"
        )


@account_switch_cmd.handle()
async def _(index: Annotated[str, EventPlainText()], state: T_State):
    user_id = state["user_id"]
    if not index.isdigit():
        await account_switch_cmd.finish(At("user", user_id) + "【Alist】输入不合法!")
    index = int(index)
    alist_accounts = state["alist_accounts"]
    if index + 1 > len(alist_accounts):
        await account_switch_cmd.finish("【Alist】输入的序号范围不合法!")
    user_account: User = state["user_account"]
    main_account = alist_accounts[index]
    AlistUserManager.remove_by_user_id(user_id)
    await user_account.set_main_account(main_account)
    await account_switch_cmd.finish(
        At("user", user_id)
        + "【Alist】您已切换到账户:\n"
        + account_info_msg(main_account)
    )
