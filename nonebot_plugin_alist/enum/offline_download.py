from enum import StrEnum


class DeletePolicy(StrEnum):
    SUCCEED = "delete_on_upload_succeed"
    FAILED = "delete_on_upload_failed"
    NEVER = "delete_never"
    ALWAYS = "delete_always"


class DownloadTool(StrEnum):
    ARIA2 = "aria2"
    HTTP = "SimpleHttp"
    QBITTORRENT = "qBittorrent"
