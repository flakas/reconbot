from unittest import TestCase
from unittest.mock import Mock
from reconbot.eve import Eve

class EveTest(TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.eve = Eve(self.db_mock)

    def test_get_moon_by_id(self):
        moon = {
            'itemID': 40073896,
            'itemName': 'HED-GP II - Moon 1'
        }
        self.db_mock.fetchone.return_value = moon
        self.assertEqual(
            self.eve.get_moon_by_id(moon['itemID']),
            {
                'id': moon['itemID'],
                'name': moon['itemName']
            }
        )
        self.assertEqual(self.db_mock.execute.call_args[0][1][0], moon['itemID'])
        self.assertTrue(self.db_mock.fetchone.called)

    def test_get_planet_by_id(self):
        planet = {
            'itemID': 40073894,
            'itemName': 'HED-GP I',
            'solarSystemID': 30001161,
        }
        self.db_mock.fetchone.return_value = planet
        self.assertEqual(
            self.eve.get_planet_by_id(planet['itemID']),
            {
                'id': planet['itemID'],
                'name': planet['itemName'],
                'system_id': planet['solarSystemID']
            }
        )
        self.assertEqual(self.db_mock.execute.call_args[0][1][0], planet['itemID'])
        self.assertTrue(self.db_mock.fetchone.called)

    def test_get_system_by_id(self):
        system = {
            'itemID': 30001161,
            'itemName': 'HED-GP',
        }
        self.db_mock.fetchone.return_value = system
        self.assertEqual(
            self.eve.get_system_by_id(system['itemID']),
            {
                'id': system['itemID'],
                'name': system['itemName']
            }
        )
        self.assertEqual(self.db_mock.execute.call_args[0][1][0], system['itemID'])
        self.assertTrue(self.db_mock.fetchone.called)

    def test_get_item_by_id(self):
        item = {
            'typeID': 12235,
            'typeName': 'Amarr Control Tower'
        }
        self.db_mock.fetchone.return_value = item
        self.assertEqual(
            self.eve.get_item_by_id(item['typeID']),
            {
                'id': item['typeID'],
                'name': item['typeName']
            }
        )
        self.assertEqual(self.db_mock.execute.call_args[0][1][0], item['typeID'])
        self.assertTrue(self.db_mock.fetchone.called)
