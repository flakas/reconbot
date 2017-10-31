import requests
import base64
import functools
import datetime
import time

class ESI:
    def __init__(self, sso):
        self.sso = sso
        self.esi_server = 'https://esi.tech.ccp.is'

    @functools.lru_cache()
    def get_alliance(self, alliance_id):
        url = '/latest/alliances/%d/' % alliance_id
        return self.esi_get(url)

    @functools.lru_cache()
    def get_corporation(self, corporation_id):
        url = '/latest/corporations/%d/' % corporation_id
        return self.esi_get(url)

    @functools.lru_cache()
    def get_character(self, character_id):
        url = '/latest/characters/%d/' % character_id
        return self.esi_get(url)

    def get_notifications(self):
        url = '/latest/characters/%d/notifications/' % self.sso.character_id
        return self.esi_get(url)

    def get_new_notifications(self, max_age=None):
        notifications = self.get_notifications()
        return sorted(
            filter(
                lambda notification: self.is_recent_notification(notification['timestamp'], max_age) is True,
                notifications),
            key=lambda notification: notification['timestamp'])

    def is_recent_notification(self, timestamp, max_age=None):
        if not max_age:
            return True

        now = datetime.datetime.utcnow()
        event_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        difference = now - event_time
        return difference.total_seconds() < max_age

    @functools.lru_cache()
    def get_structure(self, structure_id):
        url = '/latest/universe/structures/%d/' % structure_id
        return self.esi_get(url)

    @functools.lru_cache()
    def get_moon(self, moon_id):
        return self.esi_get(
            '/latest/universe/moons/%d/' % moon_id
        )

    @functools.lru_cache()
    def get_planet(self, planet_id):
        return self.esi_get(
            '/latest/universe/planets/%d/' % planet_id
        )

    @functools.lru_cache()
    def get_system(self, system_id):
        return self.esi_get(
            '/latest/universe/systems/%d/' % system_id
        )

    @functools.lru_cache()
    def get_item(self, item_id):
        return self.esi_get(
            '/latest/universe/types/%d/' % item_id
        )

    def esi_get(self, endpoint, query={}):
        max_attempts = 3
        failed_request_delay = 10

        query['token'] = self.sso.get_access_token()
        query['datasource'] = 'tranquility'

        url = '%s%s' % (self.esi_server, endpoint)

        for attempt in range(1, max_attempts + 1):
            r = requests.get(url, params=query)

            if r.status_code == 200:
                response = r.json()
                return response
            elif r.status_code >= 500 and r.status_code < 600 and attempt < max_attempts:
                json = r.json()
                if r.status_code == 500 and 'response' in json:
                    return json['response']
                print('Delaying as server recovery attempt')
                time.sleep(failed_request_delay)
                continue
            else:
                print(r.headers)
                r.raise_for_status()
