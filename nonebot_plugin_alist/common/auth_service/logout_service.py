from typing import Optional

from ...context.alist_user import AlistUser, AlistUserManager
from ...models import AlistAccount


async def logout_and_switch_main_account(
    alist_user: AlistUser,
) -> Optional[AlistAccount]:
    user_account = alist_user.user_account
    main_account = await user_account.get_main_account()
    main_account.token = None
    await main_account.save()
    await user_account.reset_main_account()
    AlistUserManager.remove_by_user_id(alist_user.user_account.user_id)
    return await user_account.get_main_account()
