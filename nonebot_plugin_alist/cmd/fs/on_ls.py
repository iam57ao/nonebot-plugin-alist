from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At, Match

from ..alist_cmd import alist_cmd
from ...api.fs import fs_list
from ...context import AlistUser
from ...dependency import get_alist_user
from ...message import file_list_msg

ls_cmd = alist_cmd.dispatch("ls")


@ls_cmd.handle()
async def _(
        event: Event,
        alist_user: Annotated[AlistUser, Depends(get_alist_user)],
        page: Match[int]
):
    user_id = event.get_user_id()
    main_account = await alist_user.user_account.get_main_account()
    path = alist_user.path
    page_num = page.result if page.available else 1
    resp_body = await fs_list(alist_user, path, page=page_num)
    if resp_body["code"] != 200:
        await ls_cmd.finish(
            At("user", user_id) +
            f"【Alist】目录预览失败! 错误信息: {resp_body['message']}"
        )
    file_list = resp_body["data"]["content"]
    if not file_list:
        await ls_cmd.finish(
            At("user", user_id) +
            "【Alist】该目录下无任何内容!"
        )
    await ls_cmd.finish(
        At("user", user_id) +
        f"【Alist】目录预览:\n"
        f"站点: {main_account.site_url}\n"
        f"当前目录: {path}\n"
        f"内容 第{page_num}页:\n"
        f"{file_list_msg(file_list)}"
    )
