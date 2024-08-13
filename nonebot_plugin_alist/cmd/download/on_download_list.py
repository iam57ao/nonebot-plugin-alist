from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At

from ...api.admin.task import download_done, download_undone
from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...message.task import task_list_msg
from ..alist_commands import alist_cmd

download_list_cmd = alist_cmd.dispatch("download.list")


@download_list_cmd.handle()
async def _(event: Event, alist_user: Annotated[AlistUser, Depends(get_alist_user)]):
    done_resp_body = await download_done(alist_user)
    undone_resp_body = await download_undone(alist_user)
    user_id = event.get_user_id()
    if error_message := _get_error_message(done_resp_body, undone_resp_body):
        await download_list_cmd.finish(
            At("user", user_id) + f"【Alist】查询失败! 错误信息: {error_message}"
        )
    down_list = undone_resp_body["data"] + done_resp_body["data"]
    if down_list:
        await download_list_cmd.finish(
            At("user", user_id) + "【Alist】离线下载列表:\n" + task_list_msg(down_list)
        )
    else:
        await download_list_cmd.finish(At("user", user_id) + "【Alist】暂无离线下载!")


def _get_error_message(done_resp_body: dict, undone_resp_body: dict) -> str:
    if done_resp_body["code"] != 200:
        return done_resp_body["message"]
    if undone_resp_body["code"] != 200:
        return undone_resp_body["message"]
    return ""
