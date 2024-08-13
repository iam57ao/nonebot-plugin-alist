from arclet.alconna import command_manager

from ..alist_commands import alist_cmd

help_cmd = alist_cmd.dispatch("help")


@help_cmd.handle()
async def help_cmd_handle():
    cmd = command_manager.get_command("alist")
    await help_cmd.finish(cmd.get_help())
