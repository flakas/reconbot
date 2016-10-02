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

        self.game_masters_corporation = {
            'id': 216121397,
            'name': 'Game Masters',
            'alliance_id': 434243723
        }

        self.ccp_falcon = {
            'id': 92532650,
            'name': 'CCP Falcon',
            'corp': self.ccp_corporation,
            'alliance': self.ccp_alliance
        }

        self.hed_gp = {
            'id': 30001161,
            'name': 'HED-GP',
            'region': 10000014
        }

        self.hed_gp_planet = {
            'id': 40073894,
            'name': 'HED-GP I',
            'system_id': self.hed_gp['id'],
        }

        self.hed_gp_moon = {
            'id': 40073896,
            'name': 'HED-GP II - Moon 1'
        }

        self.amarr_control_tower = {
            'id': 12235,
            'name': 'Amarr Control Tower'
        }

        self.fitting_service = {
            'id': 28155,
            'name': 'Fitting Service'
        }

        self.ihub = {
            'id': 32458,
            'name': 'Infrastructure Hub'
        }

        self.station = {
            'id': 1529,
            'name': 'Caldari Administrative Station'
        }

        self.astrahus = {
            'id': 35832,
            'name': 'Astrahus'
        }

        self.campaign_event_types = {
            'tcu': 1,
            'ihub': 2,
            'station': 3
        }

        self.standup_cloning_center = {
            'id': 35894,
            'name': 'Standup Cloning Center I'
        }

        self.eve_mock.get_alliance_name_by_id.return_value = self.ccp_alliance['name']
        self.eve_mock.get_corporation_name_by_id.return_value = self.ccp_corporation['name']
        self.eve_mock.get_character_by_id.return_value = self.ccp_falcon
        self.eve_mock.get_system_by_id.return_value = self.hed_gp
        self.eve_mock.get_planet_by_id.return_value = self.hed_gp_planet
        self.eve_mock.get_moon_by_id.return_value = self.hed_gp_moon
        self.eve_mock.get_item_by_id.return_value = self.amarr_control_tower

    def test_get_alliance(self):
        self.assertEqual(
            self.printer.get_alliance(self.ccp_alliance['id']),
            '<https://zkillboard.com/alliance/434243723/|C C P Alliance>'
        )

        self.eve_mock.get_alliance_name_by_id.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_corporation_without_alliance(self):
        self.assertEqual(
            self.printer.get_corporation(self.ccp_corporation['id']),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding>'
        )

        self.eve_mock.get_corporation_name_by_id.assert_called_once_with(
            self.ccp_corporation['id']
        )

    def test_get_corporation_with_alliance(self):
        self.assertEqual(
            self.printer.get_corporation(
                self.ccp_corporation['id'],
                self.ccp_alliance['id']
            ),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

        self.eve_mock.get_corporation_name_by_id.assert_called_once_with(
            self.ccp_corporation['id']
        )
        self.eve_mock.get_alliance_name_by_id.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_character(self):
        self.assertEqual(
            self.printer.get_character(self.ccp_falcon['id']),
            '<https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

        self.eve_mock.get_character_by_id.assert_called_once_with(
            self.ccp_falcon['id']
        )
        self.eve_mock.get_corporation_name_by_id.assert_called_once_with(
            self.ccp_corporation['id']
        )
        self.eve_mock.get_alliance_name_by_id.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_system(self):
        self.assertEqual(
            self.printer.get_system(self.hed_gp['id']),
            '<http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system_by_id.assert_called_once_with(
            self.hed_gp['id']
        )

    def test_get_planet(self):
        self.assertEqual(
            self.printer.get_planet(self.hed_gp_planet['id']),
            'HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system_by_id.assert_called_once_with(
            self.hed_gp['id']
        )

    def test_get_item(self):
        self.assertEqual(
            self.printer.get_item(self.amarr_control_tower['id']),
            'Amarr Control Tower'
        )

        self.eve_mock.get_item_by_id.assert_called_once_with(
            self.amarr_control_tower['id']
        )

    def test_get_campaign_event_type(self):
        self.assertEqual(
            self.printer.get_campaign_event_type(self.campaign_event_types['tcu']),
            'TCU'
        )

        self.assertEqual(
            self.printer.get_campaign_event_type(self.campaign_event_types['ihub']),
            'IHUB'
        )

        self.assertEqual(
            self.printer.get_campaign_event_type(self.campaign_event_types['station']),
            'Station'
        )

        self.assertEqual(
            self.printer.get_campaign_event_type(9999),
            'Unknown structure type "9999"'
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

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV acquired in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_pos_anchoring_alert(self):
        notification = {
            'notification_type': 45,
            'corpID': self.ccp_corporation['id'],
            'allianceID': self.ccp_alliance['id'],
            'moonID': self.hed_gp_moon['id']
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'New POS anchored in "HED-GP II - Moon 1" by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_pos_attack(self):
        notification = {
            'notification_type': 75,
            'moonID': self.hed_gp_moon['id'],
            'aggressorID': self.ccp_falcon['id'],
            'typeID': self.amarr_control_tower['id'],
            'shieldValue': 0.917,
            'armorValue': 0.91,
            'hullValue': 0.903,
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'HED-GP II - Moon 1 POS "Amarr Control Tower" (91.7% shield, 91.0% armor, 90.3% hull) under attack by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_station_conquered(self):
        notification = {
            'notification_type': 79,
            'solarSystemID': self.hed_gp['id'],
            'oldOwnerID': self.ccp_corporation['id'],
            'newOwnerID': self.ccp_corporation['id'],
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Station conquered from <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_poco_attack(self):
        notification = {
            'notification_type': 93,
            'planetID': self.hed_gp_planet['id'],
            'aggressorID': self.ccp_falcon['id'],
            'shieldLevel': 0.917,
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            '"HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>" POCO (91% shields) has been attacked by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_poco_reinforce(self):
        notification = {
            'notification_type': 94,
            'planetID': self.hed_gp_planet['id'],
            'aggressorID': self.ccp_falcon['id'],
            'reinforceExitTime': 131189759320000000
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            '"HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>" POCO has been reinforced by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)) (comes out of reinforce on "2016-09-21 23:58:52")'
        )

    def test_structure_transfer(self):
        self.eve_mock.get_corporation_name_by_id.side_effect = lambda ID: self.game_masters_corporation['name'] if ID is self.game_masters_corporation['id'] else self.ccp_corporation['name']
        notification = {
            'notification_type': 95,
            'fromCorporationName': self.game_masters_corporation['name'],
            'fromCorporationLinkData': ['showinfo', 2, self.game_masters_corporation['id']],
            'toCorporationName': self.ccp_corporation['name'],
            'toCorporationLinkData': ['showinfo', 2, self.ccp_corporation['id']],
            'structureName': 'HED-GP Freeport Citadel',
            'structureLinkData': ['showinfo', self.astrahus['id'], 1021121988766],
            'solarSystemName': self.hed_gp['name'],
            'solarSystemLinkData': ['showinfo', 5, self.hed_gp['id']],
            'characterName': self.ccp_falcon['name'],
            'characterLinkData': ['showinfo', 1377, self.ccp_falcon['id']],
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            '"HED-GP Freeport Citadel" structure in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been transferred from <https://zkillboard.com/corporation/216121397/|Game Masters> to <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_entosis_capture_started(self):
        self.eve_mock.get_item_by_id.return_value = self.fitting_service
        notification = {
            'notification_type': 147,
            'solarSystemID': self.hed_gp['id'],
            'structureTypeID': self.fitting_service['id']
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Capturing of "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has started'
        )

    def test_entosis_enabled_structure(self):
        self.eve_mock.get_item_by_id.return_value = self.fitting_service
        notification = {
            'notification_type': 148,
            'solarSystemID': self.hed_gp['id'],
            'structureTypeID': self.fitting_service['id']
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Structure "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been enabled'
        )

    def test_entosis_disabled_structure(self):
        self.eve_mock.get_item_by_id.return_value = self.fitting_service
        notification = {
            'notification_type': 149,
            'solarSystemID': self.hed_gp['id'],
            'structureTypeID': self.fitting_service['id']
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Structure "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been disabled'
        )

    def test_sov_structure_reinforced(self):
        notification = {
            'notification_type': 160,
            'solarSystemID': self.hed_gp['id'],
            'campaignEventType': self.campaign_event_types['tcu'],
            'decloakTime': 131189759320000000
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "TCU" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been reinforced, nodes will decloak "2016-09-21 23:58:52"'
        )

    def test_sov_structure_command_nodes_decloaked(self):
        notification = {
            'notification_type': 161,
            'solarSystemID': self.hed_gp['id'],
            'campaignEventType': self.campaign_event_types['tcu'],
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Command nodes for "TCU" SOV structure in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> have decloaked'
        )

    def test_sov_structure_destroyed(self):
        self.eve_mock.get_item_by_id.return_value = self.ihub
        notification = {
            'notification_type': 162,
            'solarSystemID': self.hed_gp['id'],
            'structureTypeID': self.ihub['id']
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "Infrastructure Hub" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been destroyed'
        )

        self.eve_mock.get_item_by_id.assert_called_once_with(
            self.ihub['id']
        )

    def test_sov_structure_freeported(self):
        self.eve_mock.get_item_by_id.return_value = self.station
        notification = {
            'notification_type': 163,
            'solarSystemID': self.hed_gp['id'],
            'structureTypeID': self.station['id'],
            'freeportexittime': 131189759320000000
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "Caldari Administrative Station" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been freeported, exits freeport on "2016-09-21 23:58:52"'
        )

        self.eve_mock.get_item_by_id.assert_called_once_with(
            self.station['id']
        )

    def test_citadel_low_fuel(self):
        notification = {
            'notification_type': 181,
            'solarsystemID': self.hed_gp['id'],
            'listOfTypesAndQty': [[149, 4247]],
            'structureID': 1021121988766,
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel low fuel alert in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_citadel_anchored(self):
        notification = {
            'notification_type': 182,
            'solarsystemID': self.hed_gp['id'],
            'vulnerableTime': 9000000000,
            'timeLeft': 864000385106,
            'ownerCorpName': self.ccp_corporation['name'],
            'ownerCorpLinkData': ['showinfo', 2, self.ccp_corporation['id']],
            'structureID': 1021121988766,
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel anchored in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding>'
        )

    def test_citadel_attacked(self):
        notification = {
            'notification_type': 184,
            'solarsystemID': self.hed_gp['id'],
            'structureID': 1021121988766,
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766],
            'charID': self.ccp_falcon['id'],
            'allianceName': self.ccp_alliance['name'],
            'shieldPercentage': 5.459048365958682e-13,
            'corpLinkData': ['showinfo', 2, self.ccp_corporation['id']],
            'allianceID': self.ccp_alliance['id'],
            'allianceLinkData': ['showinfo', 16159, self.ccp_alliance['id']],
            'corpName': self.ccp_corporation['name'],
            'hullPercentage': 99.79458190646601,
            'armorPercentage': 0.0
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel attacked (0.0% shield, 0.0% armor, 99.8% hull) in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_citadel_onlined(self):
        notification = {
            'notification_type': 185,
            'solarsystemID': self.hed_gp['id'],
            'structureID': 1021121988766,
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel onlined in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_citadel_destroyed(self):
        notification = {
            'notification_type': 188,
            'solarsystemID': self.hed_gp['id'],
            'structureID': 1021121988766,
            'ownerCorpLinkData': ['showinfo', 2, self.ccp_corporation['id']],
            'ownerCorpName': self.ccp_corporation['name'],
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021911646506]
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel destroyed in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> owned by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding>'
        )

    def test_citadel_out_of_fuel(self):
        self.eve_mock.get_item_by_id.return_value = self.standup_cloning_center
        notification = {
            'notification_type': 198,
            'listOfServiceModuleIDs': [self.standup_cloning_center['id']],
            'solarsystemID': self.hed_gp['id'],
            'structureID': 1021121988766,
            'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel ran out of fuel in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> with services "Standup Cloning Center I"'
        )
        self.eve_mock.get_item_by_id.assert_called_once_with(
            self.standup_cloning_center['id']
        )
