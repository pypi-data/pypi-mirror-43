class LoginFailed(Exception):
    """When login attempt failed"""


class NoMatches(Exception):
    """When filtering to find object id results in zero matches"""


class MoreThanOneMatch(Exception):
    """When filtering to find object id results in more then one object"""


class NotLoggedInOrSessionExpired(Exception):
    """When result of request to django admin endpoint is redirect to login"""


class DjangoAdminInvalidRequest(Exception):
    """When django admin complains about some errors in the input"""

    def __init__(self, message, response=None, errors=None):
        super().__init__(message)
        self.response = response
        self.errors = errors


class MissingRequiredArgument(Exception):
    """When missing required arguments when adding new model object"""


class PassedUnrecognizedArguments(Exception):
    """When passed unrecognized arguments to add new model object request"""
