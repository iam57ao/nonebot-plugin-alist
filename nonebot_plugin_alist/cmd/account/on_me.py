from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot_plugin_alconna import At

from ..alist_cmd import alist_cmd
from ...context import AlistUser
from ...dependency import get_alist_user
from ...enum import DeletePolicy
from ...message import account_info_msg

me_cmd = alist_cmd.dispatch("me")


@me_cmd.handle()
async def handle_event(
        event: Event,
        alist_user: Annotated[AlistUser, Depends(get_alist_user)]
):
    main_account = await alist_user.user_account.get_main_account()
    path = alist_user.path
    download_tool = alist_user.download_tool.name
    delete_policy_names = {
        DeletePolicy.SUCCEED: "上传成功后删除",
        DeletePolicy.FAILED: "上传失败时删除",
        DeletePolicy.NEVER: "从不删除",
        DeletePolicy.ALWAYS: "总是删除"
    }
    delete_policy_name = delete_policy_names.get(alist_user.delete_policy)
    user_info_message = (
        f"【Alist】用户信息:\n"
        f"当前账户:\n{account_info_msg(main_account)}\n"
        f"当前目录: {path}\n"
        f"离线下载:\n"
        f"-工具: {download_tool}\n"
        f"-删除策略: {delete_policy_name}"
    )
    await me_cmd.finish(
        At("user", event.get_user_id()) +
        user_info_message
    )
