from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends, EventPlainText
from nonebot.typing import T_State

from ...common.download_option_service import handle_change, handle_selection
from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...enum.offline_download import DownloadTool
from ..alist_commands import alist_cmd

download_tool_cmd = alist_cmd.dispatch("download.tool")


@download_tool_cmd.handle()
async def _(
    event: Event,
    alist_user: Annotated[AlistUser, Depends(get_alist_user)],
    state: T_State,
):
    download_tool_options = {
        DownloadTool.ARIA2: "Aria2",
        DownloadTool.HTTP: "SimpleHttp",
        DownloadTool.QBITTORRENT: "qBittorrent",
    }
    await handle_selection(
        event,
        alist_user,
        state,
        download_tool_options,
        alist_user.download_tool,
        download_tool_cmd,
        "下载工具",
    )


@download_tool_cmd.handle()
async def _(index: Annotated[str, EventPlainText()], state: T_State):
    await handle_change(index, state, download_tool_cmd, "下载工具", "download_tool")
