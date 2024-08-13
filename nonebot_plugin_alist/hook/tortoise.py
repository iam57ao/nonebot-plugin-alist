import os

from nonebot import get_driver
from tortoise import Tortoise

from ..models import AlistAccount, User

driver = get_driver()


@driver.on_startup
async def db_connect():
    if not os.path.exists("alist"):
        os.mkdir("alist")
    await Tortoise.init(
        db_url="sqlite://alist/data.db",
        modules={"models": [AlistAccount.__module__, User.__module__]},
    )
    await Tortoise.generate_schemas()


@driver.on_shutdown
async def db_close():
    await Tortoise.close_connections()
