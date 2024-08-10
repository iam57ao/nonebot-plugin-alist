from typing import Optional

from tortoise import fields
from tortoise.models import Model


class AlistAccount(Model):
    account_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='alist_accounts', on_delete=fields.CASCADE)
    site_url = fields.TextField()
    site_username = fields.TextField()
    token = fields.TextField(null=True)


class User(Model):
    user_id = fields.CharField(pk=True, max_length=255)
    alist_accounts = fields.ReverseRelation[AlistAccount]
    main_account_id = fields.IntField(null=True)

    async def set_main_account(self, alist_account: AlistAccount):
        self.main_account_id = alist_account.account_id
        await self.save()

    async def get_main_account(self) -> Optional[AlistAccount]:
        return await AlistAccount.get_or_none(account_id=self.main_account_id)

    async def clear_main_account(self):
        self.main_account_id = None
        await self.save()

    async def reset_main_account(self):
        """
        从该用户已有的账户中选取一个已经登录的账户作为主账户。
        如果没有符合条件的账户，则将主账户清空。
        """
        await self.fetch_related("alist_accounts")
        for logged_account in self.alist_accounts:
            if logged_account.token:
                await self.set_main_account(logged_account)
                break
        else:
            await self.clear_main_account()
