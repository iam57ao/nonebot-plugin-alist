from typing import Annotated

from nonebot.adapters import Event
from nonebot.params import Depends, EventPlainText
from nonebot.typing import T_State

from ...common.download_option_service import handle_change, handle_selection
from ...context.alist_user import AlistUser
from ...dependency import get_alist_user
from ...enum.offline_download import DeletePolicy
from ..alist_commands import alist_cmd

download_policy_cmd = alist_cmd.dispatch("download.policy")


@download_policy_cmd.handle()
async def handle_policy_selection(
    event: Event,
    alist_user: Annotated[AlistUser, Depends(get_alist_user)],
    state: T_State,
):
    delete_policy_options = {
        DeletePolicy.SUCCEED: "上传成功后删除",
        DeletePolicy.FAILED: "上传失败时删除",
        DeletePolicy.NEVER: "从不删除",
        DeletePolicy.ALWAYS: "总是删除",
    }
    await handle_selection(
        event,
        alist_user,
        state,
        delete_policy_options,
        alist_user.delete_policy,
        download_policy_cmd,
        "删除策略",
    )


@download_policy_cmd.handle()
async def handle_policy_change(index: Annotated[str, EventPlainText()], state: T_State):
    await handle_change(index, state, download_policy_cmd, "删除策略", "delete_policy")
