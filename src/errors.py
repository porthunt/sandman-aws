class Error(Exception):
    default_message = ""

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message if message else self.default_message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"statusCode": self.status_code, "message": self.message}


class UnknownError(Error):
    status_code = 500
    default_message = "Unknown error occurred"
