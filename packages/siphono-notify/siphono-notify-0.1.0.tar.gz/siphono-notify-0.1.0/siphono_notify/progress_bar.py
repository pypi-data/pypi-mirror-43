"""Module for progress bar."""
from siphono_notify import client


class ProgressBar(object):
    """A named progress bar aimed at a specific target."""

    def __init__(self, target_token: str, name: str):
        """
        Initialize the progress bar.

        :param target_token:
            The siphono target token. This is expected to be composed of
            4 words. i.e. correct-horse-battery-staple.
        :param name:
            The name of the progress bar. Ths should identify the job or
            process who's progress is being monitored.
        """
        self._token = target_token
        self._name = name
        self._message = None

    def update(self, progress: float, message: str = None):
        """
        Update the progress bar.

        :param progress:
            A number from 0 to 1 denoting the progress. 0 correlates to 0% and
            1 correlates to 100%.
        :param message:
            A short message to associate with the progress bar update. This
            may be used to denote the stage that the job or process is
            currently in. If no message is given then the previous value
            will be used.
        """
        self._message = message if message is not None else self._message
        self._message = None if self._message == '' else self._message
        client.send_progress_bar(
            self._token, self._name, progress, self._message
        )
