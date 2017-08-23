from slackclient import SlackClient

#
#
#
def sendSlack(channel, token, message):

    sc = SlackClient(token)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )
