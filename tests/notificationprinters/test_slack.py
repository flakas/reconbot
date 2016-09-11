from unittest import TestCase
from unittest.mock import Mock

from reconbot.notificationprinters.slack import Slack

class SlackTest(TestCase):
    def setUp(self):
        self.eve_mock = Mock()
        self.printer = Slack(self.eve_mock)

        self.timestamp = 1451649600 # 2016-01-01 12:00:00

        self.ccp_alliance = {
            'id': 434243723,
            'name': 'C C P Alliance'
        }

        self.ccp_corporation = {
            'id': 98356193,
            'name': 'C C P Alliance Holding',
            'alliance_id': 434243723
        }

        self.hed_gp = {
            'id': 30001161,
            'name': 'HED-GP',
            'region': 10000014
        }

    def test_get_alliance(self):
        alliance_id = self.ccp_alliance['id']
        alliance_name = self.ccp_alliance['name']

        self.eve_mock.alliance_id_to_name.return_value = alliance_name

        self.assertEqual(
            self.printer.get_alliance(alliance_id),
            '<https://zkillboard.com/alliance/434243723/|C C P Alliance>'
        )

        self.eve_mock.alliance_id_to_name.assert_called_once_with(
            alliance_id
        )

    def test_get_corporation_without_alliance(self):
        corporation_id = self.ccp_corporation['id']
        corporation_name = self.ccp_corporation['name']

        self.eve_mock.corporation_id_to_name.return_value = corporation_name

        self.assertEqual(
            self.printer.get_corporation(corporation_id),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding>'
        )

        self.eve_mock.corporation_id_to_name.assert_called_once_with(
            corporation_id
        )

    def test_get_corporation_with_alliance(self):
        corporation_id = self.ccp_corporation['id']
        corporation_name = self.ccp_corporation['name']
        alliance_id = self.ccp_alliance['id']
        alliance_name = self.ccp_alliance['name']

        self.eve_mock.corporation_id_to_name.return_value = corporation_name
        self.eve_mock.alliance_id_to_name.return_value = alliance_name

        self.assertEqual(
            self.printer.get_corporation(corporation_id, alliance_id),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

        self.eve_mock.corporation_id_to_name.assert_called_once_with(
            corporation_id
        )
        self.eve_mock.alliance_id_to_name.assert_called_once_with(
            alliance_id
        )

    def test_get_system(self):
        system_id = self.hed_gp['id']
        system_name = self.hed_gp['name']

        self.eve_mock.get_system_by_id.return_value = self.hed_gp

        self.assertEqual(
            self.printer.get_system(system_id),
            '<http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system_by_id.assert_called_once_with(
            system_id
        )

    def test_transforms_unknown_notification_type(self):
        notification = {
            'notification_type': 9999,
            'notification_timestamp': self.timestamp
        }

        self.assertEqual(
            self.printer.transform(notification),
            '[2016-01-01 12:00:00] Unknown notification type for printing'
        )

    def test_sov_claim_lost(self):
        notification = {
            'notification_type': 41,
            'corpID': self.ccp_corporation['id'],
            'allianceID': self.ccp_alliance['id'],
            'solarSystemID': self.hed_gp['id']
        }

        self.eve_mock.get_system_by_id.return_value = self.hed_gp
        self.eve_mock.corporation_id_to_name.return_value = self.ccp_corporation['name']
        self.eve_mock.alliance_id_to_name.return_value = self.ccp_alliance['name']

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV lost in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_sov_claim_acquired(self):
        notification = {
            'notification_type': 43,
            'corpID': self.ccp_corporation['id'],
            'allianceID': self.ccp_alliance['id'],
            'solarSystemID': self.hed_gp['id']
        }

        self.eve_mock.get_system_by_id.return_value = self.hed_gp
        self.eve_mock.corporation_id_to_name.return_value = self.ccp_corporation['name']
        self.eve_mock.alliance_id_to_name.return_value = self.ccp_alliance['name']

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV acquired in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )
