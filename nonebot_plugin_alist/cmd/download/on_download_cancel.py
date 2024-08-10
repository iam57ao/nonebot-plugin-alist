from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At, Match

from ..alist_cmd import alist_cmd
from ...api.admin.task import download_cancel, download_delete
from ...context import AlistUser
from ...dependency import get_alist_user

download_cancel_cmd = alist_cmd.dispatch("download.cancel")


@download_cancel_cmd.handle()
async def _(
        event: Event,
        alist_user: Annotated[AlistUser, Depends(get_alist_user)],
        tid: Match[str]
):
    tid = tid.result
    user_id = event.get_user_id()
    resp_body = await download_cancel(alist_user, tid)
    if resp_body["code"] != 200:
        await download_cancel_cmd.finish(
            At("user", user_id) +
            f"【Alist】取消失败! 错误信息: {resp_body['message']}"
        )
    else:
        await download_delete(alist_user, tid)
        await download_cancel_cmd.finish(
            At("user", user_id) +
            f"【Alist】取消ID为{tid}的任务成功!"
        )
