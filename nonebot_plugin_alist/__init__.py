from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from . import cmd, hook
from .config import Config

__all__ = ["cmd", "hook"]
__plugin_meta__ = PluginMetadata(
    name="Alist",
    description="一个支持多账号的Alist管理插件",
    usage="发送命令/alist help查看帮助",
    type="application",
    homepage="https://github.com/iam57ao/nonebot-plugin-alist",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
