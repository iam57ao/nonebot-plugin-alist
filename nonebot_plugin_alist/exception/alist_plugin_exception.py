class AlistPluginException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"AlistPluginException: {self.message}"