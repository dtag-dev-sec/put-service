from slackclient import SlackClient

#
# simple Slack sender for status reports
#
def sendSlack(channel, token, message):

    if channel is None or token is None or message is None:
        return

    sc = SlackClient(token)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )
