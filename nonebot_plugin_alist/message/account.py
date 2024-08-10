from ..models import AlistAccount


def account_info_msg(account: AlistAccount) -> str:
    return (
        f"站点: {account.site_url}\n"
        f"用户名: {account.site_username}\n"
        f"登录状态: {'已登录' if account.token else '未登录'}"
    )


def account_list_msg(accounts: list[AlistAccount]) -> str:
    account_list = [
        f"序号: {index}\n{account_info_msg(account)}"
        for index, account in enumerate(accounts)
    ]
    if account_list:
        return "\n".join(account_list)
    else:
        return "没有账户!"
