class BaseException(Exception):
    pass


class AlreadyExistsError(BaseException):
    pass

class NotFoundError(BaseException):
    pass
