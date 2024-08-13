from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At

from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ..alist_commands import alist_cmd

pwd_cmd = alist_cmd.dispatch("pwd")


@pwd_cmd.handle()
async def _(event: Event, alist_user: Annotated[AlistUser, Depends(get_alist_user)]):
    main_account = await alist_user.user_account.get_main_account()
    await pwd_cmd.finish(
        At("user", event.get_user_id()) + f"【Alist】目录信息:\n"
        f"站点: {main_account.site_url}\n"
        f"当前目录: {alist_user.path}"
    )
