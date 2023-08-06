from requests import HTTPError


class ClientError(Exception):
    """The client is not ready to make this request."""


class StateError(ClientError):
    """A required parent entity has not been set."""


class ServerError(Exception):
    """The server is not able to complete this request."""


class NotFoundError(ServerError):
    """The requested entity could not be found."""
