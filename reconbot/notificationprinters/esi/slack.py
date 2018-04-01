import abc
import requests
from reconbot.notificationprinters.esi.printer import Printer

class Slack(Printer):

    def get_corporation(self, corporation_id):
        corporation = self.eve.get_corporation(corporation_id)
        result = '<https://zkillboard.com/corporation/%d/|%s>' % (corporation_id, corporation['name'])

        if 'alliance_id' in corporation:
            result = '%s (%s)' % (result, self.get_alliance(corporation['alliance_id']))

        return result

    def get_alliance(self, alliance_id):
        alliance = self.eve.get_alliance(alliance_id)
        return '<https://zkillboard.com/alliance/%d/|%s>' % (alliance_id, alliance['name'])

    def get_system(self, system_id):
        system = self.eve.get_system(system_id)
        return '<http://evemaps.dotlan.net/system/%s|%s>' % (system['name'], system['name'])

    def get_character(self, character_id):
        try:
            character = self.eve.get_character(character_id)
        except requests.HTTPError as ex:
            # Patch for character being unresolvable and ESI throwing internal errors
            # Temporarily stub character to not break our behavior.
            if ex.response.status_code == 500:
                character = { 'name': 'Unknown character', 'corporation_id': 98356193 }
            else:
                raise

        return '<https://zkillboard.com/character/%d/|%s> (%s)' % (
            character_id,
            character['name'],
            self.get_corporation(character['corporation_id'])
        )

    def get_killmail(self, killmail_id, killmail_hash):
        killmail = self.eve.get_killmail(killmail_id, killmail_hash)
        victim = self.get_character(killmail['victim']['character_id'])
        ship = self.get_item(killmail['victim']['ship_type_id'])
        system = self.get_system(killmail['solar_system_id'])

        return '%s lost a(n) %s in %s (<https://zkillboard.com/kill/%d/|Zkillboard>)' % (
            victim,
            ship,
            system,
            killmail_id
        )
