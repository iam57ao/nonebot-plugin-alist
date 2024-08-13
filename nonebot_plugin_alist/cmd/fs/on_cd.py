import os
from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At, Match

from ...api.fs import dirs
from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ..alist_commands import alist_cmd

cd_cmd = alist_cmd.dispatch("cd")


def resolve_path(base_path: str, cd_path: str) -> str:
    final_path = os.path.normpath(os.path.join(base_path, cd_path))
    return final_path.replace("\\", "/")


@cd_cmd.handle()
async def _(
    event: Event,
    alist_user: Annotated[AlistUser, Depends(get_alist_user)],
    path: Match[str],
):
    user_id = event.get_user_id()
    if not path.available:
        await cd_cmd.finish(At("user", user_id) + "【Alist】未输入路径!")
    new_path = resolve_path(alist_user.path, path.result)
    resp_body = await dirs(alist_user, new_path)
    if resp_body["code"] != 200:
        await cd_cmd.finish(
            At("user", user_id)
            + f"【Alist】目录切换失败! 错误信息: {resp_body['message']}"
        )
    alist_user.path = new_path
    await cd_cmd.finish(At("user", user_id) + f"【Alist】当前目录: {new_path}")
