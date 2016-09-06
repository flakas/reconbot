from slacker import Slacker

class SlackNotifier:
    def __init__(self, api_key, name, default_channel, default_priority='normal'):
        self.api_key = api_key
        self.name = name
        self.default_channel = default_channel
        self.slack = Slacker(self.api_key)
        self.default_priority = default_priority

    def notify(self, text, options={}):
        if self.default_priority == 'all':
            text_template = "<!channel>:\n%s"
        elif self.default_priority == 'online':
            text_template = "<!here>:\n%s"
        else:
            text_template = "%s"

        if 'channel' in options:
            channel = options['channel']
        else:
            channel = self.default_channel

        self.slack.chat.post_message(
                channel,
                text_template % text,
                parse="none",
                username=self.name
                )
