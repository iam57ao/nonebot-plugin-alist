from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends, EventPlainText
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...enum.offline_download import DownloadTool
from ..alist_commands import alist_cmd

download_tool_cmd = alist_cmd.dispatch("download.tool")


@download_tool_cmd.handle()
async def handle_tool_selection(
    event: Event,
    alist_user: Annotated[AlistUser, Depends(get_alist_user)],
    state: T_State,
):
    user_id = event.get_user_id()
    download_tool_options = {
        DownloadTool.ARIA2: "Aria2",
        DownloadTool.HTTP: "SimpleHttp",
        DownloadTool.QBITTORRENT: "qBittorrent",
    }
    state.update(
        {
            "download_tool_options": download_tool_options,
            "user_id": user_id,
            "alist_user": alist_user,
        }
    )
    current_tool_name = download_tool_options[alist_user.download_tool]
    download_tool_options.pop(alist_user.download_tool)
    available_tools_message = [
        f"{index} {tool_name}"
        for index, tool_name in enumerate(download_tool_options.values())
    ]
    await download_tool_cmd.pause(
        At("user", user_id)
        + f"【Alist】当前下载工具: {current_tool_name}\n"
        + "请输入序号修改:\n"
        + "\n".join(available_tools_message)
        + "\n输入 '取消' 取消更改!"
    )


@download_tool_cmd.handle()
async def handle_tool_change(index: Annotated[str, EventPlainText()], state: T_State):
    user_id = state["user_id"]
    if index == "取消":
        await download_tool_cmd.finish(At("user", user_id) + "【Alist】已取消更改!")
    download_tool_options: dict[DownloadTool, str] = state["download_tool_options"]
    if not index.isdigit():
        await download_tool_cmd.finish(At("user", user_id) + "【Alist】输入不合法!")
    selected_index = int(index)
    available_tools = list(download_tool_options.keys())
    if selected_index >= len(available_tools):
        await download_tool_cmd.finish("【Alist】输入的序号范围不合法!")
    alist_user: AlistUser = state["alist_user"]
    alist_user.download_tool = available_tools[selected_index]
    await download_tool_cmd.finish(
        At("user", user_id)
        + f"【Alist】您已切换下载工具为: {list(download_tool_options.values())[selected_index]}"
    )
