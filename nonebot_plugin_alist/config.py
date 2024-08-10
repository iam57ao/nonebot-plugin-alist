from pydantic import BaseModel


class Config(BaseModel):
    alist_request_timeout: int = 10
