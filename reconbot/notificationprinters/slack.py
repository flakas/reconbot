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
        pass

    def get_system(self, system_id):
        system = self.eve.get_system_by_id(system_id)
        return '<http://evemaps.dotlan.net/system/%s|%s>' % (system['name'], system['name'])

    def get_character(self, character_id):
        pass

    def timestamp_to_date(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
