from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At, Match

from ..alist_cmd import alist_cmd
from ...api.fs import add_offline_download
from ...context import AlistUser
from ...dependency import get_alist_user
from ...enum import DeletePolicy, DownloadTool
from ...message import task_list_msg

download_add_cmd = alist_cmd.dispatch("download.add")


@download_add_cmd.handle()
async def _(
        event: Event,
        alist_user: Annotated[AlistUser, Depends(get_alist_user)],
        urls: Match[str]
):
    urls = urls.result.split("\n")
    tool_values = {
        DownloadTool.ARIA2: "aria2",
        DownloadTool.HTTP: "SimpleHttp",
        DownloadTool.QBITTORRENT: "qBittorrent"
    }
    delete_policy_values = {
        DeletePolicy.SUCCEED: "delete_on_upload_succeed",
        DeletePolicy.FAILED: "delete_on_upload_failed",
        DeletePolicy.NEVER: "delete_never",
        DeletePolicy.ALWAYS: "delete_always"
    }
    path = alist_user.path
    tool = tool_values[alist_user.download_tool]
    delete_policy = delete_policy_values[alist_user.delete_policy]
    resp_body = await add_offline_download(
        alist_user,
        urls,
        path,
        tool,
        delete_policy
    )
    user_id = event.get_user_id()
    if resp_body["code"] != 200:
        await download_add_cmd.finish(
            At("user", user_id) +
            f"【Alist】添加失败! 错误信息: {resp_body['message']}"
        )
    data = resp_body["data"]
    tasks: list = data["tasks"]
    await download_add_cmd.finish(
        At("user", user_id) +
        f"【Alist】添加成功{len(tasks)}个任务!\n"
        f"{task_list_msg(tasks)}"
    )
