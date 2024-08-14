from typing import Any, Dict, TypeVar

from nonebot.adapters import Event
from nonebot.typing import T_State
from nonebot_plugin_alconna import At

T = TypeVar("T")


async def handle_selection(
    event: Event,
    alist_user: Any,
    state: T_State,
    options: Dict[T, str],
    current_option: T,
    command,
    option_type: str,
):
    user_id = event.get_user_id()
    state.update(
        {
            f"{option_type}_options": options,
            "user_id": user_id,
            "alist_user": alist_user,
        }
    )
    current_option_name = options[current_option]
    options.pop(current_option)
    available_options_message = [
        f"{index} {option_name}" for index, option_name in enumerate(options.values())
    ]
    await command.pause(
        At("user", user_id)
        + f"【Alist】当前{option_type}: {current_option_name}\n"
        + "请输入序号修改:\n"
        + "\n".join(available_options_message)
        + "\n输入 '取消' 取消更改!"
    )


async def handle_change(
    index: str,
    state: T_State,
    command,
    option_type: str,
    attribute_name: str,
):
    user_id = state["user_id"]
    if index == "取消":
        await command.finish(At("user", user_id) + f"【Alist】已取消{option_type}更改!")
    options: dict = state[f"{option_type}_options"]
    if not index.isdigit():
        await command.finish(At("user", user_id) + "【Alist】输入不合法!")
    selected_index = int(index)
    available_options = list(options.keys())
    if selected_index >= len(available_options):
        await command.finish("【Alist】输入的序号范围不合法!")
    alist_user = state["alist_user"]
    setattr(alist_user, attribute_name, available_options[selected_index])
    await command.finish(
        At("user", user_id)
        + f"【Alist】您已切换{option_type}为: {list(options.values())[selected_index]}"
    )
