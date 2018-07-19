import yaml
from unittest import TestCase
from unittest.mock import Mock, call

from reconbot.notificationprinters.esi.formatter import Formatter

class SlackTest(TestCase):
    def setUp(self):
        self.printer = Mock()
        self.notification = {
            'againstID': 12345,
            'declaredByID': 23456
        }

        self.formatter = Formatter(self.printer, self.notification)

    def test_calls_printer_method_with_given_arg(self):
        self.printer.corporation_or_alliance.return_value = 'Some Corp'

        'War declared against {:corporation_or_alliance(againstID)}'.format(self.formatter)

        self.printer.corporation_or_alliance.assert_called_once_with(
            self.notification['againstID']
        )

    def test_calls_printer_method_with_multiple_given_args(self):
        self.printer.get_killmail.return_value = 'Some Killmail'

        'Erebus was killed {0:get_killmail(againstID, declaredByID)}'.format(self.formatter)

        self.printer.get_killmail.assert_called_once_with(
            self.notification['againstID'],
            self.notification['declaredByID']
        )

    def test_formats_text_with_given_arg(self):
        self.printer.corporation_or_alliance.return_value = 'Some Corp'

        self.assertEqual(
            'War declared against {:corporation_or_alliance(againstID)}'.format(self.formatter),
            'War declared against Some Corp'
        )

    def test_using_unknown_method_raises_exception(self):
        self.printer.unknown_method.side_effect = Exception("AttributeError: 'dict' object has no attribute 'unknown_method'")

        with self.assertRaises(Exception):
            'War declared against {:unknown_method(againstID)}'.format(self.formatter)

    def test_using_unknown_attribute_raises_exception(self):
        with self.assertRaises(Exception):
            'War declared against {:some_method(unknown_attribute)}'.format(self.formatter)
