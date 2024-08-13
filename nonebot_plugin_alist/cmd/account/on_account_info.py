from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At

from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...message.account import account_info_msg
from ..alist_commands import alist_cmd

account_info_cmd = alist_cmd.dispatch("account.info")


@account_info_cmd.handle()
async def _(event: Event, alist_user: Annotated[AlistUser, Depends(get_alist_user)]):
    main_account = await alist_user.user_account.get_main_account()
    await account_info_cmd.finish(
        At("user", event.get_user_id())
        + "【Alist】当前账户:\n"
        + account_info_msg(main_account)
    )
