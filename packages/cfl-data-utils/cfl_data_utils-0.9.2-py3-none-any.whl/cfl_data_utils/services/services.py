from requests import post


def stub(*args, **kwargs):
    """Stubbed function!

    :param args:
    :param kwargs:
    """
    pass


def slack(webhook_url: str, m: str):
    """Send a Slack message to a Slackbot

    :param webhook_url: Webhook of Slackbot
    :param m: The message
    """

    post(webhook_url, headers={'Content-Type': 'application/json'}, json={'text': m})
