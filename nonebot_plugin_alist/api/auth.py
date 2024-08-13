from ..context.alist_user import AlistUser
from ..request import async_client, authenticated_client


async def login_hash(site_url: str, username: str, password_hash: str):
    async with async_client(site_url) as client:
        resp = await client.post(
            "/api/auth/login/hash",
            json={"username": username, "password": password_hash},
        )
        return resp.json()


async def me(alist_user: AlistUser):
    async with await authenticated_client(alist_user) as client:
        resp = await client.get("/api/me")
        return resp.json()
