from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import EventPlainText
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

from ...context.alist_user import AlistUserManager
from ...message.account import account_info_msg, account_list_msg
from ...models import AlistAccount, User
from ..alist_commands import alist_cmd

account_del_cmd = alist_cmd.dispatch("account.del")


@account_del_cmd.handle()
async def _(event: Event, state: T_State):
    user_id = event.get_user_id()
    user_account = await User.get_or_none(user_id=user_id)
    if not user_account:
        await account_del_cmd.finish(
            At("user", user_id) + "【Alist】您没有需要删除的账户!"
        )
    await user_account.fetch_related("alist_accounts")
    alist_accounts = user_account.alist_accounts
    if not alist_accounts:
        await account_del_cmd.finish(
            At("user", user_id) + "【Alist】您没有需要删除的账户!"
        )
    else:
        state.update(
            {
                "user_id": user_id,
                "user_account": user_account,
                "alist_accounts": alist_accounts,
            }
        )
        await account_del_cmd.pause(
            At("user", user_id)
            + "【Alist】请回复要重新登录的账户序号或序号集 (空格分割):\n"
            + account_list_msg(alist_accounts)
        )


@account_del_cmd.handle()
async def _(index_list: Annotated[str, EventPlainText()], state: T_State):
    user_id = state["user_id"]
    index_list = set(index_list.split(" "))
    if not all(index.isdigit() for index in index_list):
        await account_del_cmd.finish(At("user", user_id) + "【Alist】输入不合法!")
    alist_accounts = state["alist_accounts"]
    max_index = len(alist_accounts) - 1
    index_list = map(int, index_list)
    del_account_id = [
        alist_accounts[index].account_id for index in index_list if index <= max_index
    ]
    if del_account_id:
        await AlistAccount.filter(account_id__in=del_account_id).delete()
        await account_del_cmd.send(At("user", user_id) + "【Alist】删除成功!")
        user_account: User = state["user_account"]
        if user_account.main_account_id in del_account_id:
            await user_account.reset_main_account()
            AlistUserManager.remove_by_user_id(user_id)
            main_account = await user_account.get_main_account()
            if main_account:
                await account_del_cmd.finish(
                    At("user", user_id)
                    + "【Alist】您已切换到账户:\n"
                    + account_info_msg(main_account)
                )
            else:
                await account_del_cmd.finish(
                    At("user", user_id) + "【Alist】没有可以切换的账户!"
                )
    else:
        await account_del_cmd.finish(At("user", user_id) + "【Alist】删除失败!")
