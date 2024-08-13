from typing import Annotated

from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.params import ArgStr
from nonebot_plugin_alconna import At
from pydantic import HttpUrl, ValidationError

from ...common.auth_service.login_service import login
from ...context.alist_user import AlistUserManager
from ...exception.auth_exception import AuthException
from ...message.account import account_info_msg
from ...models import AlistAccount, User
from ..alist_commands import alist_cmd

account_add_cmd = alist_cmd.dispatch("account.add")


@account_add_cmd.handle()
async def _(event: GroupMessageEvent):
    await account_add_cmd.finish(
        At("user", event.get_user_id()) + "【Alist】请私聊添加账户!"
    )


@account_add_cmd.got("site_url", prompt="【Alist】请输入您的Alist首页URL地址")
@account_add_cmd.got("username", prompt="【Alist】请输入您的Alist用户名")
@account_add_cmd.got("password", prompt="【Alist】请输入您的Alist密码")
async def _(
    site_url: Annotated[str, ArgStr()],
    username: Annotated[str, ArgStr()],
    password: Annotated[str, ArgStr()],
    event: Event,
):
    try:
        HttpUrl(site_url)
    except ValidationError:
        await account_add_cmd.finish("【Alist】URL格式错误!")
    site_url = site_url.rstrip("/")
    try:
        token = await login(site_url, username, password)
    except AuthException as e:
        await account_add_cmd.finish(f"【Alist】添加失败! 错误信息: {e.message}")
    else:
        (user, _) = await User.get_or_create(user_id=event.get_user_id())
        (alist_account, created) = await AlistAccount.get_or_create(
            user=user, site_url=site_url, site_username=username
        )
        if not created:
            await account_add_cmd.finish("【Alist】无法添加已存在的账户!")
        alist_account.token = token
        user_id = event.get_user_id()
        await alist_account.save()
        await user.set_main_account(alist_account)
        AlistUserManager.remove_by_user_id(user_id)
        await account_add_cmd.finish("【Alist】添加成功!")
        await account_add_cmd.finish(
            At("user", user_id)
            + "【Alist】您已切换到账户:\n"
            + account_info_msg(alist_account)
        )
