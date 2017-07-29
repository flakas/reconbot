import datetime
import requests
import evelink.api
import yaml

# Use Yaml parser for EVE response structures
evelink.api.parse_keyval_data = lambda data_string: yaml.load(data_string)

class Eve:
    def __init__(self, db, eve_api, character_api=None):
        self.db = db
        self.eve_api = eve_api
        self.character_api = character_api

    def get_moon_by_id(self, moon_id):
        self.db.execute("SELECT * FROM mapDenormalize WHERE itemID=?", (moon_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
        }

    def get_planet_by_id(self, planet_id):
        self.db.execute("SELECT itemID, itemName, solarSystemID FROM mapDenormalize WHERE itemID=?", (planet_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
            'system_id': location['solarSystemID'],
        }

    def get_system_by_id(self, system_id):
        self.db.execute("SELECT itemID, itemName FROM mapDenormalize WHERE itemID=?", (system_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
        }

    def get_item_by_id(self, item_id):
        self.db.execute("SELECT typeID, typeName FROM invTypes WHERE typeID=?", (item_id,))
        item = self.db.fetchone()
        return {
            'id': item['typeID'],
            'name': item['typeName'],
        }

    def get_alliance_name_by_id(self, alliance_id):
        return self.eve_api.character_names_from_ids(alliance_id).result[alliance_id]

    def get_corporation_name_by_id(self, corporation_id):
        return self.eve_api.character_names_from_ids(corporation_id).result[corporation_id]

    def get_character_by_id(self, character_id):
        return self.eve_api.affiliations_for_character(character_id).result

    def get_notifications(self, max_age=None):
        notifications = self.character_api.notifications().result
        new_notifications = self.get_new_notifications(notifications, max_age)
        return self.get_notification_texts(new_notifications)

    def get_new_notifications(self, notifications, max_age=None):
        return dict(filter(
          lambda notification: self.is_recent_notification(notification[1]['timestamp'], max_age) is True,
          notifications.items()))

    def get_notification_texts(self, notifications):
        notification_ids = list(notifications.keys())

        if len(notification_ids) == 0:
            return {}

        notification_texts = self.character_api.notification_texts(notification_ids=notification_ids).result

        for notification_id, notification in notifications.items():
            if notification_id not in notification_texts:
                continue
            notification_texts[notification_id]['notification_timestamp'] = notification['timestamp']

            if 'notification_type' not in notification_texts[notification_id]:
                notification_texts[notification_id]['notification_type'] = notification['type_id']
                notification_texts[notification_id]['notification_id'] = notification_id

        return sorted(notification_texts.values(), key=lambda item: item['notification_timestamp'])

    def is_recent_notification(self, timestamp, max_age=None):
        if not max_age:
            return True

        now = datetime.datetime.utcnow()
        event_time = datetime.datetime.utcfromtimestamp(timestamp)
        difference = now - event_time
        return difference.total_seconds() < max_age

    def get_structure_by_id(self, structure_id):
        structure_id = str(structure_id)
        try:
            r = requests.get('https://stop.hammerti.me.uk/api/citadel/%s' % structure_id)
            json = r.json()
            if not isinstance(json, dict):
                return {}
            if structure_id not in json:
                return {}
            return json[structure_id]
        except Exception as ex:
            return {}
