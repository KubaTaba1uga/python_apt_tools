from copy import copy


class PackageNotFoundError(BaseException):
    MESSAGE = """Package could not be found."""

    def __init__(self):
        self.message = copy(self.MESSAGE)
        super(PackageNotFoundError, self).__init__(self.message)
