import datetime

class Slack:

    def __init__(self, eve):
        self.eve = eve

    def transform(self, notification):
        text = self.get_notification_text(notification)
        timestamp = self.timestamp_to_date(notification['notification_timestamp'])

        return '[%s] %s' % (timestamp, text)

    def get_notification_text(self, notification):
        if notification['notification_type'] is 41:
            return self.sov_claim_lost(notification)
        if notification['notification_type'] is 43:
            return self.sov_claim_acquired(notification)
        if notification['notification_type'] is 45:
            return self.pos_anchoring_alert(notification)
        if notification['notification_type'] is 75:
            return self.pos_attack(notification)
        if notification['notification_type'] is 79:
            return self.station_conquered(notification)
        if notification['notification_type'] is 93:
            return self.customs_office_attacked(notification)
        if notification['notification_type'] is 94:
            return self.customs_office_reinforced(notification)
        if notification['notification_type'] is 95:
            return self.structure_transferred(notification)
        if notification['notification_type'] is 147:
            return self.entosis_capture_started(notification)
        if notification['notification_type'] is 148:
            return self.entosis_enabled_structure(notification)
        if notification['notification_type'] is 149:
            return self.entosis_disabled_structure(notification)
        else:
            return 'Unknown notification type for printing'

    # 41
    def sov_claim_lost(self, notification):
        owner = self.get_corporation(notification['corpID'], notification['allianceID'])
        system = self.get_system(notification['solarSystemID'])

        return 'SOV lost in %s by %s' % (system, owner)

    # 43
    def sov_claim_acquired(self, notification):
        owner = self.get_corporation(notification['corpID'], notification['allianceID'])
        system = self.get_system(notification['solarSystemID'])

        return 'SOV acquired in %s by %s' % (system, owner)

    # 45
    def pos_anchoring_alert(self, notification):
        owner = self.get_corporation(notification['corpID'], notification['allianceID'])
        moon = self.eve.get_moon_by_id(notification['moonID'])

        return 'New POS anchored in "%s" by %s' % (moon['name'], owner)

    # 75
    def pos_attack(self, notification):
        moon = self.eve.get_moon_by_id(notification['moonID'])
        attacker = self.get_character(notification['aggressorID'])
        item_type = self.get_item(notification['typeID'])

        return "%s POS \"%s\" (%.1f%% shield, %.1f%% armor, %.1f%% hull) under attack by %s" % (
            moon['name'],
            item_type,
            notification['shieldValue']*100,
            notification['armorValue']*100,
            notification['hullValue']*100,
            attacker
        )

    # 79
    def station_conquered(self, notification):
        system = self.get_system(notification['solarSystemID'])
        old_owner = self.get_corporation(notification['oldOwnerID'])
        new_owner = self.get_corporation(notification['newOwnerID'])

        return "Station conquered from %s by %s in %s" % (old_owner, new_owner, system)

    # 93 - poco attacked
    def customs_office_attacked(self, notification):
        attacker = self.get_character(notification['aggressorID'])
        planet = self.get_planet(notification['planetID'])
        shields = int(notification['shieldLevel']*100)

        return "\"%s\" POCO (%d%% shields) has been attacked by %s" % (planet, shields, attacker)

    # 94 - poco reinforced
    def customs_office_reinforced(self, notification):
        attacker = self.get_character(notification['aggressorID'])
        planet = self.get_planet(notification['planetID'])
        timestamp = self.eve_timestamp_to_date(notification['reinforceExitTime'])

        return "\"%s\" POCO has been reinforced by %s (comes out of reinforce on \"%s\")" % (planet, attacker, timestamp)

    # 95 - structure (not necessarily POCO) transferred
    def structure_transferred(self, notification):
        from_corporation = notification['fromCorporationName']
        to_corporation = notification['toCorporationName']
        structure = notification['structureName']
        system = ''
        if 'solarSystemName' in notification:
          system = "in " + notification['solarSystemName']

        return "\"%s\" structure %s has been transferred from \"%s\" to \"%s\"" % (structure, system, from_corporation, to_corporation)

    # 147 - entosis capture started
    def entosis_capture_started(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Capturing of \"%s\" in %s has started" % (structure, system)

    # 148 - entosis has enabled structure
    def entosis_enabled_structure(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Structure \"%s\" in %s has been enabled" % (structure, system)

    # 149 - entosis has disabled structure
    def entosis_disabled_structure(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Structure \"%s\" in %s has been disabled" % (structure, system)

    def get_corporation(self, corporation_id, alliance_id=None):
        name = self.eve.corporation_id_to_name(corporation_id)
        result = '<https://zkillboard.com/corporation/%d/|%s>' % (corporation_id, name)

        if alliance_id:
            result = '%s (%s)' % (result, self.get_alliance(alliance_id))

        return result

    def get_alliance(self, alliance_id):
        name = self.eve.alliance_id_to_name(alliance_id)
        return '<https://zkillboard.com/alliance/%d/|%s>' % (alliance_id, name)

    def get_item(self, item_id):
        item = self.eve.get_item_by_id(item_id)
        return item['name']

    def get_system(self, system_id):
        system = self.eve.get_system_by_id(system_id)
        return '<http://evemaps.dotlan.net/system/%s|%s>' % (system['name'], system['name'])

    def get_planet(self, planet_id):
        planet = self.eve.get_planet_by_id(planet_id)
        system = self.get_system(planet['system_id'])
        return '%s in %s' % (planet['name'], system)

    def get_character(self, character_id):
        character = self.eve.get_character_by_id(character_id)

        return '<https://zkillboard.com/character/%d/|%s> (%s)' % (
            character['id'],
            character['name'],
            self.get_corporation(character['corp']['id'], character['alliance']['id'])
        )

    def timestamp_to_date(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def eve_timestamp_to_date(self, microseconds):
        """
        Convert microsoft epoch to unix epoch
        Based on: http://www.wiki.eve-id.net/APIv2_Char_NotificationTexts_XML
        """

        seconds = microseconds/10000000 - 11644473600
        return datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')
