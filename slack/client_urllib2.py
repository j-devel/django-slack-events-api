import urllib
import urllib2

import logging
logging.getLogger().setLevel(logging.INFO)


class Client():
    def __init__(self, slack_bot_token):
        self.slack_bot_token = slack_bot_token

    def chat_post_message(self, channel, text):
        # https://api.slack.com/methods/chat.postMessage
        #     Present these parameters as part of
        #     an application/x-www-form-urlencoded querystring or POST body.
        #     application/json is not currently accepted.
        data = {
            'token': self.slack_bot_token,
            'channel': channel,
            'text': text
        }
        req = urllib2.Request('https://slack.com/api/chat.postMessage')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_data(urllib.urlencode(data))
        response = urllib2.urlopen(req)
        logging.info("response: %s" % response.read())
