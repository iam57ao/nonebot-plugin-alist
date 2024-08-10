from .alist_plugin_exception import AlistPluginException


class AuthException(AlistPluginException):
    def __init__(self, message):
        super().__init__(message)
