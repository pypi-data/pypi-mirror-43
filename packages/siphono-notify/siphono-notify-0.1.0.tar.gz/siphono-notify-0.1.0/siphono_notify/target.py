"""Module defining a messaging target."""
from siphono_notify.notifier import Notifier
from siphono_notify.progress_bar import ProgressBar


class Target(object):
    """A target to interact with."""

    def __init__(self, token: str):
        """
        Initialize the target.

        :param token:
            The siphono notify token. This is expected to be composed of
            4 words. i.e. correct-horse-battery-staple.
        """
        self._token = token

    def notifier(self, name: str) -> Notifier:
        """
        Generate a notifier for the target.

        :param name:
            The name to assign to the notifier.
        :return:
            A notifier for the target.
        """
        return Notifier(self._token, name)

    def progress_bar(self, name: str) -> ProgressBar:
        """
        Generate a progress bar for the target.

        :param name:
            The name of the progress bar.
        :return:
            A progress bar for the target.
        """
        return ProgressBar(self._token, name)
