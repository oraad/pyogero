"""Exceptions for the Ogero module."""


class OgeroError(Exception):
    """Base error for Ogero."""


class AuthenticationException(OgeroError):
    """Authentication error for Ogero."""


class OgeroCommunicationError(OgeroError):
    """Communication error when contacting Ogero."""


class OgeroParseError(OgeroError):
    """Error parsing Ogero HTML or JSON responses."""
