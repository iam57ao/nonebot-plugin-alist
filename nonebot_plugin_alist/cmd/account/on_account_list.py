from nonebot.adapters import Event
from nonebot_plugin_alconna import At

from ..alist_cmd import alist_cmd
from ...message import account_list_msg
from ...models import User

account_list_cmd = alist_cmd.dispatch("account.list")


@account_list_cmd.handle()
async def _(event: Event):
    user_account = await User.get_or_none(user_id=event.get_user_id())
    if user_account:
        await user_account.fetch_related("alist_accounts")
        alist_accounts = user_account.alist_accounts
    else:
        alist_accounts = []
    await account_list_cmd.finish(
        At("user", event.get_user_id()) +
        f"【Alist】我的账户:\n" +
        account_list_msg(alist_accounts)
    )