"""Client module for messaging backend notify api."""
import requests

from siphono_notify import configs


def send_notification(
        target_token: str, group_name: str, title: str, body: str
):
    """
    Send a notification at the specified target.

    :param target_token:
        A token identifying the device to send the notification to.
    :param group_name:
        The name of the group associated with the notification. This should
        be useful in identifing the process send the message.
    :param title:
        The title of the notification.
    :param body:
        The main content of the notification.
    """
    url = '{host}/targets/{id}/notifications'.format(
        host=configs.NOTIFY_API,
        id=target_token,
    )
    requests.post(
        url, json={'group': group_name, 'title': title, 'body': body}
    )


def send_progress_bar(
        target_token: str,
        name: str,
        progress: float,
        message: str = None,
):
    """
    Send a progress bar to the specified target.

    :param target_token:
        A token identifying the device to send the notification to.
    :param name:
        The name of the progress bar. Ths should identify the job or process
        who's progress is being monitored.
    :param progress:
        A number from 0 to 1 denoting the progress. 0 correlates to 0% and
        1 correlates to 100%.
    :param message:
        A short message to associate with the progress bar update. This may
        be used to denote the stage that the job or process is currently in.
    """
    progress_bar_id = name + '+' + target_token
    url = '{host}/progress-bars/{id}'.format(
        host=configs.NOTIFY_API,
        id=progress_bar_id,
    )
    requests.put(url, json={'message': message, 'progress': progress})
