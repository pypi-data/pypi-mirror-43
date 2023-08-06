"""Definition of the notifier element for sending notifications."""
import functools
import traceback
import typing

from siphono_notify import client


class Notifier(object):
    """A named notifier aimed at a specific target."""

    def __init__(self, target_token: str, name: str):
        """
        Initialize the notifier.

        :param target_token:
            The siphono notify token. This is expected to be composed of
            4 words. i.e. correct-horse-battery-staple.
        :param name:
            The name of the notifier. This should identify the source of the
            notification.
        """
        self._token = target_token
        self._name = name

    def send(self, title: str, message: str):
        """
        Send a notification to the target

        :param title:
            The title of the notification being sent.
        :param message:
            The message body of the notification being sent
        """
        client.send_notification(self._token, self._name, title, message)

    def relay_exceptions(self, func: typing.Callable) -> typing.Callable:
        """
        Decorate a function to catch all errors coming from it, send them
        as notifications, and reraise the error.

        :param func:
            The function to decorate. All exceptions originating from the
            function will be caught and sent as notifications.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Catch any exception, send it as a notification and then reraise
            the exception.
            """
            try:
                return func(*args, **kwargs)
            except Exception as err:
                title = str(err) or type(err).__name__ or 'Error'
                msg = traceback.format_exc(limit=100)
                client.send_notification(self._token, self._name, title, msg)
                raise

        return wrapper
