__author__="Dario Incalza <dario@overture.ai"
__copyright__="Copyright 2018, Overture"
__version__="0.0.1"
__maintainer__="Dario Incalza"
__email__="dario@overture.ai"


class RestApiError(Exception):
    def __init__(self, message, statuscode):
        super().__init__(message)
        self.statuscode = statuscode
        self.message = message

    def __str__(self):
        return "[ApiError] - [{}] - {}".format(self.statuscode, self.message)
