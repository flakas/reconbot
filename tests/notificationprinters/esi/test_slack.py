import yaml
from unittest import TestCase
from unittest.mock import Mock, call

from reconbot.notificationprinters.esi.slack import Slack

class SlackTest(TestCase):
    def setUp(self):
        self.eve_mock = Mock()
        self.printer = Slack(self.eve_mock)

        self.timestamp = '2018-01-01T12:00:00Z'

        self.ccp_alliance = {
            'id': 434243723,
            'name': 'C C P Alliance'
        }

        self.corp_without_alliance = {
            'id': 998877654,
            'name': 'Allianceless Corporation',
        }

        self.ccp_corporation = {
            'id': 98356193,
            'name': 'C C P Alliance Holding',
            'alliance_id': self.ccp_alliance['id']
        }

        self.game_masters_corporation = {
            'id': 216121397,
            'name': 'Game Masters',
            'alliance_id': self.ccp_alliance['id']
        }

        self.ccp_falcon = {
            'id': 92532650,
            'name': 'CCP Falcon',
            'corporation_id': self.ccp_corporation['id'],
            'alliance_id': self.ccp_alliance['id']
        }

        self.ccp_someone = {
            'id': 92532651,
            'name': 'CCP Someone',
            'corporation_id': self.ccp_corporation['id']
        }

        self.character_without_alliance = {
            'id': 92532650,
            'name': 'CCP allianceless',
            'corporation_id': self.corp_without_alliance['id']
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

        self.atron = {
            'id': 608,
            'name': 'Atron'
        }

        self.ichooseyou_hub_fortizar = {
            'structure_id': 1023164547009,
            'structure': {
                "typeId": 35833,
                "regionId": 10000002,
                "typeName": "Fortizar",
                "lastSeen": "2017-07-02T11:37:44.359Z",
                "firstSeen": "2017-01-13T18:07:24Z",
                "regionName": "The Forge",
                "name": "Perimeter - IChooseYou Trade Hub",
                "systemId": 30000144,
                "location": {
                    "y": 44793533020.0,
                    "x": 660596273924.0,
                    "z": 2112970671473.0},
                "systemName": "Perimeter",
                "public": True
            }
        }

        self.killmail_hash = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
        self.killmail = {
            'killmail_id': 123,
            'victim': {
                'character_id': self.ccp_falcon['id'],
                'ship_type_id': self.atron['id']
            },
            'solar_system_id': self.hed_gp['id']
        }

        self.eve_mock.get_alliance.return_value = self.ccp_alliance
        self.eve_mock.get_corporation.return_value = self.ccp_corporation
        self.eve_mock.get_character.return_value = self.ccp_falcon
        self.eve_mock.get_system.return_value = self.hed_gp
        self.eve_mock.get_planet.return_value = self.hed_gp_planet
        self.eve_mock.get_moon.return_value = self.hed_gp_moon
        self.eve_mock.get_item.return_value = self.amarr_control_tower
        self.eve_mock.get_structure.return_value = self.ichooseyou_hub_fortizar['structure']
        self.eve_mock.get_killmail.return_value = self.killmail

    def test_get_alliance(self):
        self.assertEqual(
            self.printer.get_alliance(self.ccp_alliance['id']),
            '<https://zkillboard.com/alliance/434243723/|C C P Alliance>'
        )

        self.eve_mock.get_alliance.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_corporation_without_alliance(self):
        self.eve_mock.get_corporation.return_value = self.corp_without_alliance

        self.assertEqual(
            self.printer.get_corporation(self.corp_without_alliance['id']),
            '<https://zkillboard.com/corporation/998877654/|Allianceless Corporation>'
        )

        self.eve_mock.get_corporation.assert_called_once_with(
            self.corp_without_alliance['id']
        )

    def test_get_corporation_with_alliance(self):
        self.assertEqual(
            self.printer.get_corporation(
                self.ccp_corporation['id']
            ),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

        self.eve_mock.get_corporation.assert_called_once_with(
            self.ccp_corporation['id']
        )
        self.eve_mock.get_alliance.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_corporation_or_alliance_returns_corporation(self):
        self.eve_mock.get_corporation.return_value = self.corp_without_alliance

        self.assertEqual(
            self.printer.get_corporation_or_alliance(self.corp_without_alliance['id']),
            '<https://zkillboard.com/corporation/998877654/|Allianceless Corporation>'
        )

        self.eve_mock.get_corporation.assert_called_once_with(
            self.corp_without_alliance['id']
        )

    def test_get_corporation_or_alliance_returns_alliance(self):
        self.eve_mock.get_corporation.side_effect = Exception("Corporation not found")

        self.assertEqual(
            self.printer.get_corporation_or_alliance(self.ccp_alliance['id']),
            '<https://zkillboard.com/alliance/434243723/|C C P Alliance>'
        )

        self.eve_mock.get_corporation.assert_called_once_with(
            self.ccp_alliance['id']
        )
        self.eve_mock.get_alliance.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_character(self):
        self.assertEqual(
            self.printer.get_character(self.ccp_falcon['id']),
            '<https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

        self.eve_mock.get_character.assert_called_once_with(
            self.ccp_falcon['id']
        )
        self.eve_mock.get_corporation.assert_called_once_with(
            self.ccp_corporation['id']
        )
        self.eve_mock.get_alliance.assert_called_once_with(
            self.ccp_alliance['id']
        )

    def test_get_character_without_alliance(self):
        self.eve_mock.get_character.return_value = self.character_without_alliance
        self.eve_mock.get_corporation.return_value = self.corp_without_alliance
        self.assertEqual(
            self.printer.get_character(self.character_without_alliance['id']),
            '<https://zkillboard.com/character/92532650/|CCP allianceless> (<https://zkillboard.com/corporation/998877654/|Allianceless Corporation>)'
        )

    def test_get_system(self):
        self.assertEqual(
            self.printer.get_system(self.hed_gp['id']),
            '<http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system.assert_called_once_with(
            self.hed_gp['id']
        )

    def test_get_planet(self):
        self.assertEqual(
            self.printer.get_planet(self.hed_gp_planet['id']),
            'HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system.assert_called_once_with(
            self.hed_gp['id']
        )

    def test_get_moon(self):
        self.assertEqual(
            self.printer.get_moon(self.hed_gp_moon['id']),
            'HED-GP II - Moon 1'
        )

        self.eve_mock.get_moon.assert_called_once_with(
            self.hed_gp_moon['id']
        )

    def test_get_item(self):
        self.assertEqual(
            self.printer.get_item(self.amarr_control_tower['id']),
            'Amarr Control Tower'
        )

        self.eve_mock.get_item.assert_called_once_with(
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

    def test_get_structure_name(self):
        self.assertEqual(
            self.printer.get_structure_name(self.ichooseyou_hub_fortizar['structure_id']),
            self.ichooseyou_hub_fortizar['structure']['name']
        )

    def test_transforms_unknown_notification_type(self):
        notification = {
            'type': 'UnknownType',
            'timestamp': self.timestamp,
            'text': ''
        }

        self.assertEqual(
            self.printer.transform(notification),
            '[2018-01-01 12:00:00] Unknown notification type for printing'
        )

    def test_sov_claim_lost(self):
        notification = {
            'type': 'SovAllClaimLostMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'corpID': self.ccp_corporation['id'],
                'allianceID': self.ccp_alliance['id'],
                'solarSystemID': self.hed_gp['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV lost in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_corporation_war_declared(self):
        self.eve_mock.get_corporation.side_effect = lambda ID: self.game_masters_corporation if ID == self.game_masters_corporation['id'] else self.ccp_corporation
        notification = {
            'type': 'AllWarDeclaredMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'againstID': self.ccp_corporation['id'],
                'declaredByID': self.game_masters_corporation['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'War has been declared to <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>) by <https://zkillboard.com/corporation/216121397/|Game Masters> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_sov_claim_acquired(self):
        notification = {
            'type': 'SovAllClaimAquiredMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'corpID': self.ccp_corporation['id'],
                'allianceID': self.ccp_alliance['id'],
                'solarSystemID': self.hed_gp['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV acquired in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_pos_anchoring_alert(self):
        notification = {
            'type': 'AllAnchoringMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'corpID': self.ccp_corporation['id'],
                'allianceID': self.ccp_alliance['id'],
                'moonID': self.hed_gp_moon['id'],
                'typeID': self.amarr_control_tower['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'New structure (Amarr Control Tower) anchored in "HED-GP II - Moon 1" by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_pos_attack(self):
        notification = {
            'type': 'TowerAlertMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'moonID': self.hed_gp_moon['id'],
                'aggressorID': self.ccp_falcon['id'],
                'typeID': self.amarr_control_tower['id'],
                'shieldValue': 0.917,
                'armorValue': 0.91,
                'hullValue': 0.903,
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'HED-GP II - Moon 1 POS "Amarr Control Tower" (91.7% shield, 91.0% armor, 90.3% hull) under attack by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_station_conquered(self):
        notification = {
            'type': 'StationConquerMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'oldOwnerID': self.ccp_corporation['id'],
                'newOwnerID': self.ccp_corporation['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Station conquered from <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>) by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>) in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_poco_attack(self):
        notification = {
            'type': 'OrbitalAttacked',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'planetID': self.hed_gp_planet['id'],
                'aggressorID': self.ccp_falcon['id'],
                'shieldLevel': 0.917,
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            '"HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>" POCO (91.7% shields) has been attacked by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_poco_reinforce(self):
        notification = {
            'type': 'OrbitalReinforced',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'planetID': self.hed_gp_planet['id'],
                'aggressorID': self.ccp_falcon['id'],
                'reinforceExitTime': 131189759320000000
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            '"HED-GP I in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>" POCO has been reinforced by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)) (comes out of reinforce on "2016-09-21 23:58:52")'
        )

    def test_structure_transfered(self):
        self.eve_mock.get_item.return_value = self.astrahus
        self.eve_mock.get_corporation.side_effect = lambda ID: self.game_masters_corporation if ID == self.game_masters_corporation['id'] else self.ccp_corporation
        notification = {
            'type': 'OwnershipTransferred',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'charID': self.ccp_falcon['id'],
                'newOwnerCorpID': self.ccp_corporation['id'],
                'oldOwnerCorpID': self.game_masters_corporation['id'],
                'solarSystemID': self.hed_gp['id'],
                'structureID': 1021121988766,
                'structureName': 'HED-GP Freeport Citadel',
                'structureTypeID': self.astrahus['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Astrahus HED-GP Freeport Citadel structure in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been transferred from <https://zkillboard.com/corporation/216121397/|Game Masters> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>) to <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>) by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_entosis_capture_started(self):
        self.eve_mock.get_item.return_value = self.fitting_service
        notification = {
            'type': 'EntosisCaptureStarted',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'structureTypeID': self.fitting_service['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Capturing of "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has started'
        )

    def test_entosis_enabled_structure(self):
        self.eve_mock.get_item.return_value = self.fitting_service
        notification = {
            'type': 'StationServiceEnabled',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'structureTypeID': self.fitting_service['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Structure "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been enabled'
        )

    def test_entosis_disabled_structure(self):
        self.eve_mock.get_item.return_value = self.fitting_service
        notification = {
            'type': 'StationServiceDisabled',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'structureTypeID': self.fitting_service['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Structure "Fitting Service" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been disabled'
        )

    def test_sov_structure_reinforced(self):
        notification = {
            'type': 'SovStructureReinforced',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'campaignEventType': self.campaign_event_types['tcu'],
                'decloakTime': 131189759320000000
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "TCU" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been reinforced, nodes will decloak "2016-09-21 23:58:52"'
        )

    def test_sov_structure_command_nodes_decloaked(self):
        notification = {
            'type': 'SovCommandNodeEventStarted',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'campaignEventType': self.campaign_event_types['tcu'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Command nodes for "TCU" SOV structure in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> have decloaked'
        )

    def test_sov_structure_destroyed(self):
        self.eve_mock.get_item.return_value = self.ihub
        notification = {
            'type': 'SovStructureDestroyed',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'structureTypeID': self.ihub['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "Infrastructure Hub" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been destroyed'
        )

        self.eve_mock.get_item.assert_called_once_with(
            self.ihub['id']
        )

    def test_sov_structure_freeported(self):
        self.eve_mock.get_item.return_value = self.station
        notification = {
            'type': 'SovStationEnteredFreeport',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarSystemID': self.hed_gp['id'],
                'structureTypeID': self.station['id'],
                'freeportexittime': 131189759320000000
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'SOV structure "Caldari Administrative Station" in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> has been freeported, exits freeport on "2016-09-21 23:58:52"'
        )

        self.eve_mock.get_item.assert_called_once_with(
            self.station['id']
        )

    def test_citadel_low_fuel(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureFuelAlert',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'listOfTypesAndQty': [[149, 4247]],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") low fuel alert in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_citadel_low_power(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureWentLowPower',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'listOfTypesAndQty': [[149, 4247]],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766],
                'structureTypeID': self.astrahus['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") went into low power mode in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_citadel_high_power(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureWentHighPower',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'listOfTypesAndQty': [[149, 4247]],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766],
                'structureTypeID': self.astrahus['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") went into high power mode in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )


    def test_citadel_anchored(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureAnchoring',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'vulnerableTime': 9000000000,
                'timeLeft': 864000385106,
                'ownerCorpName': self.ccp_corporation['name'],
                'ownerCorpLinkData': ['showinfo', 2, self.ccp_corporation['id']],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") anchored in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_citadel_attacked(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureUnderAttack',
            'timestamp': self.timestamp,
            'text': yaml.dump({
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
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") attacked (0.0% shield, 0.0% armor, 99.8% hull) in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> by <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_citadel_onlined(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureOnline',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") onlined in <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

    def test_citadel_destroyed(self):
        self.eve_mock.get_item.return_value = self.astrahus
        notification = {
            'type': 'StructureDestroyed',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'solarsystemID': self.hed_gp['id'],
                'structureID': 1021121988766,
                'ownerCorpLinkData': ['showinfo', 2, self.ccp_corporation['id']],
                'ownerCorpName': self.ccp_corporation['name'],
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021911646506]
            })
        }

        self.maxDiff = None

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") destroyed in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> owned by <https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )

    def test_citadel_out_of_fuel(self):
        self.eve_mock.get_item.side_effect = lambda ID: self.astrahus if ID == self.astrahus['id'] else self.standup_cloning_center
        notification = {
            'type': 'StructureServicesOffline',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'listOfServiceModuleIDs': [self.standup_cloning_center['id']],
                'solarsystemID': self.hed_gp['id'],
                'structureID': 1021121988766,
                'structureShowInfoData': ['showinfo', self.astrahus['id'], 1021121988766]
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Citadel (Astrahus, "Perimeter - IChooseYou Trade Hub") ran out of fuel in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> with services "Standup Cloning Center I"'
        )
        self.eve_mock.get_item.assert_any_call(self.astrahus['id'])
        self.eve_mock.get_item.assert_any_call(self.standup_cloning_center['id'])

    def test_bounty_claimed(self):
        notification = {
            'type': 'BountyClaimMsg',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'amount': 123.4567,
                'charID': self.ccp_falcon['id']
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'A bounty of 123.46 ISK has been claimed for killing <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

    def test_kill_report_victim(self):
        self.eve_mock.get_item.return_value = self.atron
        notification = {
            'type': 'KillReportVictim',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'killMailHash': self.killmail_hash,
                'killMailID': self.killmail['killmail_id'],
                'victimShipTypeID': self.killmail['victim']['ship_type_id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Died in a(n) Atron: <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)) lost a(n) Atron in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> (<https://zkillboard.com/kill/123/|Zkillboard>)'
        )

    def test_kill_report_final_blow(self):
        self.eve_mock.get_item.return_value = self.atron
        notification = {
            'type': 'KillReportFinalBlow',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                'killMailHash': self.killmail_hash,
                'killMailID': self.killmail['killmail_id'],
                'victimShipTypeID': self.killmail['victim']['ship_type_id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Got final blow on Atron: <https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)) lost a(n) Atron in <http://evemaps.dotlan.net/system/HED-GP|HED-GP> (<https://zkillboard.com/kill/123/|Zkillboard>)'
        )

    def test_alliance_capital_changed(self):
        notification = {
            'type': 'AllianceCapitalChanged',
            'timestamp': self.timestamp,
            'text': yaml.dump({
                 'allianceID': self.ccp_alliance['id'],
                 'solarSystemID': self.hed_gp['id'],
            })
        }

        self.assertEqual(
            self.printer.get_notification_text(notification),
            'Alliance capital system of <https://zkillboard.com/alliance/434243723/|C C P Alliance> has changed to <http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )


    def test_get_percentage(self):
        self.assertEqual(self.printer.get_percentage(0.17), '17.0%')
        self.assertEqual(self.printer.get_percentage(0.176), '17.6%')
        self.assertEqual(self.printer.get_percentage(0.1768), '17.7%')

        self.assertEqual(self.printer.get_percentage(17), '17.0%')
        self.assertEqual(self.printer.get_percentage(17.6), '17.6%')
        self.assertEqual(self.printer.get_percentage(17.68), '17.7%')

    def test_get_string(self):
        self.assertEqual(self.printer.get_string(123), '123')
        self.assertEqual(self.printer.get_string(123.7), '123.7')


    def test_get_corporation_from_link(self):
        self.assertEqual(
            self.printer.get_corporation_from_link(['showinfo', 2, self.ccp_corporation['id']]),
            '<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>)'
        )
        self.eve_mock.get_corporation.assert_called_once_with(
            self.ccp_corporation['id']
        )

    def test_get_structure_type_from_link(self):
        self.eve_mock.get_item.return_value = self.astrahus
        self.assertEqual(
            self.printer.get_structure_type_from_link(['showinfo', self.astrahus['id'], 1021121988766]),
            self.astrahus['name']
        )
        self.eve_mock.get_item.assert_called_once_with(
            self.astrahus['id']
        )

    def test_get_system_from_link(self):
        self.assertEqual(
            self.printer.get_system_from_link(['showinfo', 5, self.hed_gp['id']]),
            '<http://evemaps.dotlan.net/system/HED-GP|HED-GP>'
        )

        self.eve_mock.get_system.assert_called_once_with(
            self.hed_gp['id']
        )

    def test_get_character_from_link(self):
        self.assertEqual(
            self.printer.get_character_from_link(['showinfo', 1377, self.ccp_falcon['id']]),
            '<https://zkillboard.com/character/92532650/|CCP Falcon> (<https://zkillboard.com/corporation/98356193/|C C P Alliance Holding> (<https://zkillboard.com/alliance/434243723/|C C P Alliance>))'
        )

        self.eve_mock.get_character.assert_called_once_with(
            self.ccp_falcon['id']
        )

    def test_get_pos_wants(self):
        self.assertEqual(
            self.printer.get_pos_wants([{'typeID': self.amarr_control_tower['id'], 'quantity': 5}]),
            'Amarr Control Tower: 5'
        )

    def test_get_citadel_services(self):
        self.eve_mock.get_item.return_value = self.standup_cloning_center
        self.assertEqual(
            self.printer.get_citadel_services([self.standup_cloning_center['id']]),
            self.standup_cloning_center['name']
        )

        self.eve_mock.get_item.assert_called_once_with(
            self.standup_cloning_center['id']
        )
