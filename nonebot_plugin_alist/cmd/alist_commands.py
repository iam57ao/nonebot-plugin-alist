from arclet.alconna import Alconna, Args, CommandMeta, Option, Subcommand
from nonebot_plugin_alconna import on_alconna

alist_cmd = on_alconna(
    Alconna(
        "alist",
        Subcommand("cd", Args["path#目录路径", str], help_text="进入指定目录"),
        Subcommand(
            "download",
            Subcommand(
                "add",
                Args["urls#一条或多条链接, 以空格分隔", str],
                help_text="添加一条或多条下载链接",
            ),
            Subcommand("cancel", Args["tid#任务ID", str], help_text="取消一个下载任务"),
            Subcommand("list", help_text="列出所有下载链接"),
            Subcommand("policy", help_text="修改删除策略"),
            Subcommand("tool", help_text="设置下载工具"),
            help_text="Alist离线下载的操作",
        ),
        Subcommand("help", help_text="显示所有可用命令的帮助信息"),
        Subcommand("logout", help_text="退出当前登录的Alist账户"),
        Subcommand(
            "ls",
            Option("-p|--page", Args["page#页码, 使用阿拉伯数字, 如 6", int]),
            help_text="列出当前目录的文件, 支持分页显示",
        ),
        Subcommand("me", help_text="显示当前登录的Alist账户的信息"),
        Subcommand("pwd", help_text="显示当前所在目录的路径"),
        Subcommand("relogin", help_text="重新登录一个添加过的Alist账户"),
        Subcommand(
            "account",
            Subcommand("add", help_text="添加一个新的Alist账户并切换到该账户"),
            Subcommand("del", help_text="删除一个已存在的Alist账户"),
            Subcommand("info", help_text="显示当前Alist账户的详细信息"),
            Subcommand("list", help_text="列出所有已添加的Alist账户"),
            Subcommand("switch", help_text="切换到指定的Alist账户"),
            help_text="管理Alist账户的操作, 包括添加、删除、查看信息、列出所有账户和切换账户",
        ),
        meta=CommandMeta(
            description="Alist Plugin 命令",
            usage="alist [子命令] [选项]",
            example="alist cd /downloads",
            author="iam57",
        ),
    ),
    use_cmd_sep=True,
    use_cmd_start=True,
)
