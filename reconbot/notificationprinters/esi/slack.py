import abc
from reconbot.notificationprinters.esi.printer import Printer

class Slack(Printer):

    def get_corporation(self, corporation_id):
        corporation = self.eve.get_corporation(corporation_id)
        result = '<https://zkillboard.com/corporation/%d/|%s>' % (corporation_id, corporation['corporation_name'])

        if 'alliance_id' in corporation:
            result = '%s (%s)' % (result, self.get_alliance(corporation['alliance_id']))

        return result

    def get_alliance(self, alliance_id):
        alliance = self.eve.get_alliance(alliance_id)
        return '<https://zkillboard.com/alliance/%d/|%s>' % (alliance_id, alliance['alliance_name'])

    def get_system(self, system_id):
        system = self.eve.get_system(system_id)
        return '<http://evemaps.dotlan.net/system/%s|%s>' % (system['name'], system['name'])

    def get_character(self, character_id):
        character = self.eve.get_character(character_id)

        return '<https://zkillboard.com/character/%d/|%s> (%s)' % (
            character_id,
            character['name'],
            self.get_corporation(character['corporation_id'])
        )
