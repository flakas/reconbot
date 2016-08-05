from unittest import TestCase
from unittest.mock import patch

from reconbot.notifiers.slack import SlackNotifier

@patch('reconbot.notifiers.slack.Slacker')
class SlackNotifierTest(TestCase):
    def setUp(self):
        self.username = 'myname'
        self.channel = '#mychannel'

    def test_notify_sends_chat_message(self, slacker_mock):

        notifier = SlackNotifier('myapikeyhere', self.username, self.channel)
        notifier.notify('some text')

        notifier.slack.chat.post_message.assert_called_with(
            self.channel,
            "some text",
            parse='none',
            username=self.username
        )

    def test_notify_all_mentions_channel(self, slacker_mock):
        notifier = SlackNotifier('myapikeyhere', self.username, self.channel, 'all')
        notifier.notify('some text')

        notifier.slack.chat.post_message.assert_called_with(
            self.channel,
            "<!channel>:\nsome text",
            parse='none',
            username=self.username
        )

    def test_notify_online_mentions_here(self, slacker_mock):
        notifier = SlackNotifier('myapikeyhere', self.username, self.channel, 'online')
        notifier.notify('some text')

        notifier.slack.chat.post_message.assert_called_with(
            self.channel,
            "<!here>:\nsome text",
            parse='none',
            username=self.username
        )

    def test_notify_to_custom_channel(self, slacker_mock):
        new_channel = '#myotherchannel'
        notifier = SlackNotifier('myapikeyhere', self.username, self.channel, 'online')
        notifier.notify('some text', options={ 'channel': new_channel })

        notifier.slack.chat.post_message.assert_called_with(
            new_channel,
            "<!here>:\nsome text",
            parse='none',
            username=self.username
        )
