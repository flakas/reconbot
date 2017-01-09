from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from reconbot.notifiers.caching import CachingNotifier

@patch('reconbot.notifiers.caching.time')
class SplitterNotifierTest(TestCase):
    def test_notify_passes_new_messages(self, time_mock):
        time_mock.time.return_value = 1000
        mock_notifier = Mock()
        caching_notifier = CachingNotifier(mock_notifier)

        text = 'this is a sample notification'
        caching_notifier.notify(text)

        mock_notifier.notify.assert_called_with(text, {})

    def test_notify_does_not_pass_duplicate_messages(self, time_mock):
        time_mock.time.return_value = 1000
        mock_notifier = Mock()
        caching_notifier = CachingNotifier(mock_notifier)

        text = 'this is a sample notification'
        caching_notifier.notify(text)
        caching_notifier.notify(text)

        mock_notifier.notify.assert_called_once_with(text, {})

    def test_it_allows_duplicate_messages_posted_after_expiry_time(self, time_mock):
        time_mock.time.return_value = 1000
        mock_notifier = Mock()
        caching_notifier = CachingNotifier(mock_notifier, 5)

        text = 'this is a sample notification'
        caching_notifier.notify(text)
        caching_notifier.notify(text)
        caching_notifier.notify('this is another sample notification')
        # mock_notifier.notify.assert_called_once_with(text, {})
        self.assertEqual(mock_notifier.notify.call_count, 2)

        time_mock.time.return_value = 1010
        caching_notifier.notify(text)
        caching_notifier.notify(text)
        self.assertEqual(mock_notifier.notify.call_count, 3)
