import abc
from reconbot.notificationprinters.printer import Printer

class Discord(Printer):

    def get_corporation(self, corporation_id, alliance_id=None):
        name = self.eve.get_corporation_name_by_id(corporation_id)
        result = '**%s** (https://zkillboard.com/corporation/%d/)' % (name, corporation_id)

        if alliance_id:
            result = '%s (%s)' % (result, self.get_alliance(alliance_id))

        return result

    def get_alliance(self, alliance_id):
        name = self.eve.get_alliance_name_by_id(alliance_id)
        return '**%s** (https://zkillboard.com/alliance/%d/)' % (name, alliance_id)

    def get_system(self, system_id):
        system = self.eve.get_system_by_id(system_id)
        return '**%s** (http://evemaps.dotlan.net/system/%s)' % (system['name'], system['name'])

    def get_character(self, character_id):
        character = self.eve.get_character_by_id(character_id)

        if 'alliance' in character:
            alliance_id = character['alliance']['id']
        else:
            alliance_id = None

        return '**%s** (https://zkillboard.com/character/%d/) (%s)' % (
            character['name'],
            character['id'],
            self.get_corporation(character['corp']['id'], alliance_id)
        )
