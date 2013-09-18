# -*- coding: utf-8 -*-

"""
prismic.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Prismic exceptions.

"""


class Error(Exception):
    """Base class for exceptions in this module."""

    def __str__(self):
        return self.__doc__


class InvalidTokenError(Error):
    """The provided access token is either invalid or expired"""
    pass


class AuthorizationNeededError(Error):
    """You need to provide an access token to access this repository"""
    pass


class HTTPError(Error):
    """HTTP error"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(HTTPError, self).__init__()

    def __str__(self):
        return ("Got an HTTP error %(code)d (%(message)s)" %
                {"code": self.code, "message": self.message})


class UnexpectedError(Error):
    """Unexpected error."""

    def __init__(self, message):
        self.message = message
        super(UnexpectedError, self).__init__()

    def __str__(self):
        return self.message


class RefMissing(Error):
    """You need to provide the ref parameter."""
    pass
