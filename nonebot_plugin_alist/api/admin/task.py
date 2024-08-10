from ...context import AlistUser
from ...request import authenticated_client


async def download_info(
        alist_user: AlistUser,
        tid: str
):
    async with await authenticated_client(alist_user) as client:
        resp = await client.post(
            "/api/admin/task/offline_download/info",
            params={"tid": tid}
        )
        return resp.json()


async def download_done(alist_user: AlistUser):
    async with await authenticated_client(alist_user) as client:
        resp = await client.get(
            "/api/admin/task/offline_download/done"
        )
        return resp.json()


async def download_undone(alist_user: AlistUser):
    async with await authenticated_client(alist_user) as client:
        resp = await client.get(
            "/api/admin/task/offline_download/undone"
        )
        return resp.json()


async def download_cancel(
        alist_user: AlistUser,
        tid: str
):
    async with await authenticated_client(alist_user) as client:
        resp = await client.post(
            "/api/admin/task/offline_download/cancel",
            params={"tid": tid}
        )
        return resp.json()


async def download_delete(
        alist_user: AlistUser,
        tid: str
):
    async with await authenticated_client(alist_user) as client:
        resp = await client.post(
            "/api/admin/task/offline_download/delete",
            params={"tid": tid}
        )
        return resp.json()
