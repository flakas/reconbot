from unittest import TestCase
from unittest.mock import Mock
from reconbot.notifiers.splitter import SplitterNotifier

class SplitterNotifierTest(TestCase):
    def test_notify_notifies_all_notifiers(self):
        notifier1 = Mock()
        notifier2 = Mock()
        splitter = SplitterNotifier([notifier1, notifier2])

        text = 'this is a sample notification'
        splitter.notify(text)

        notifier1.notify.assert_called_with(text, {})
        notifier2.notify.assert_called_with(text, {})
