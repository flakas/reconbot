import abc
import datetime
import yaml

from reconbot.notificationprinters.esi.formatter import Formatter

class Printer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, eve):
        self.eve = eve

    def transform(self, notification):
        text = self.get_notification_text(notification)
        timestamp = self.timestamp_to_date(notification['timestamp'])

        return '[%s] %s' % (timestamp, text)

    def get_notification_text(self, notification):

        types = {
            'AllWarDeclaredMsg': self.corporation_war_declared,
            'DeclareWar': self.declare_war,
            'AllWarInvalidatedMsg': self.corporation_war_invalidated,
            'AllyJoinedWarAggressorMsg': self.aggressor_ally_joined_war,
            'CorpWarDeclaredMsg': self.corporation_war_declared,
            'EntosisCaptureStarted': self.entosis_capture_started,
            'SovCommandNodeEventStarted': self.sov_structure_command_nodes_decloaked,
            'SovStructureDestroyed': self.sov_structure_destroyed,
            'SovStructureReinforced': self.sov_structure_reinforced,
            'StructureUnderAttack': self.citadel_attacked,
            'OwnershipTransferred': self.structure_transferred,
            'StructureOnline': self.citadel_onlined,
            'StructureDestroyed': self.citadel_destroyed,
            'StructureFuelAlert': self.citadel_low_fuel,
            'StructureAnchoring': self.citadel_anchored,
            'StructureUnanchoring': self.citadel_unanchoring,
            'StructureServicesOffline': self.citadel_out_of_fuel,
            'StructureLostShields': self.citadel_lost_shields,
            'StructureLostArmor': self.citadel_lost_armor,
            'TowerAlertMsg': self.pos_attack,
            'TowerResourceAlertMsg': self.pos_fuel_alert,
            'StationServiceEnabled': self.entosis_enabled_structure,
            'StationServiceDisabled': self.entosis_disabled_structure,
            'OrbitalReinforced': self.customs_office_reinforced,
            'OrbitalAttacked': self.customs_office_attacked,
            'SovAllClaimAquiredMsg': self.sov_claim_acquired,
            'SovStationEnteredFreeport': self.sov_structure_freeported,
            'AllAnchoringMsg': self.structure_anchoring_alert,
            'InfrastructureHubBillAboutToExpire': self.ihub_bill_about_to_expire,
            'SovAllClaimLostMsg': self.sov_claim_lost,
            'SovStructureSelfDestructRequested': self.sov_structure_started_self_destructing,
            'SovStructureSelfDestructFinished': self.sov_structure_self_destructed,
            'StationConquerMsg': self.station_conquered,
            'MoonminingExtractionStarted': self.moon_extraction_started,
            'MoonminingExtractionCancelled': self.moon_extraction_cancelled,
            'MoonminingExtractionFinished': self.moon_extraction_finished,
            'MoonminingLaserFired': self.moon_extraction_turned_into_belt,
            'MoonminingAutomaticFracture': self.moon_extraction_autofractured,
            'CorpAllBillMsg': self.corporation_bill,
            'BillPaidCorpAllMsg': self.corporation_bill_paid,
            'CharAppAcceptMsg': self.character_application_accepted,
            'CorpAppNewMsg': self.new_character_application_to_corp,
            'CharAppWithdrawMsg': self.character_application_withdrawn,
            'CharLeftCorpMsg': self.character_left_corporation,
            'CorpNewCEOMsg': self.new_corporation_ceo,
            'CorpVoteMsg': self.corporation_vote_initiated,
            'CorpVoteCEORevokedMsg': self.corporation_vote_for_ceo_revoked,
            'CorpTaxChangeMsg': self.corporation_tax_changed,
            'CorpDividendMsg': self.corporation_dividend_paid_out,
            'BountyClaimMsg': self.bounty_claimed,
            'KillReportVictim': self.kill_report_victim,
            'KillReportFinalBlow': self.kill_report_final_blow,

            # kept for older messages
            'notificationTypeMoonminingExtractionStarted': self.moon_extraction_started,
        }

        if notification['type'] in types:
            text = yaml.load(notification['text'])
            text['notification_timestamp'] = notification['timestamp']
            return types[notification['type']](text)

        return 'Unknown notification type for printing'

    def corporation_war_declared(self, notification):
        return 'War has been declared to {0:get_corporation_or_alliance(againstID)} by {0:get_corporation_or_alliance(declaredByID)}'.format(Formatter(self, notification))

    def declare_war(self, notification):
        return '{0:get_character(charID)} from {0:get_corporation_or_alliance(entityID)} has declared war to {0:get_corporation_or_alliance(defenderID)}'.format(Formatter(self, notification))


    def corporation_war_invalidated(self, notification):
        return 'War has been invalidated to {0:get_corporation_or_alliance(againstID)} by {0:get_corporation_or_alliance(declaredByID)}'.format(Formatter(self, notification))

    def aggressor_ally_joined_war(self, notification):
        return 'Ally {0:get_corporation_or_alliance(allyID)} joined the war to help {0:get_corporation_or_alliance(defenderID)} starting {0:eve_timestamp_to_date(startTime)}'.format(Formatter(self, notification))

    def sov_claim_lost(self, notification):
        return 'SOV lost in {0:get_system(solarSystemID)} by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def sov_claim_acquired(self, notification):
        return 'SOV acquired in {0:get_system(solarSystemID)} by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def pos_anchoring_alert(self, notification):
        return 'New POS anchored in "{0:get_moon(moonID)}" by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def pos_attack(self, notification):
        return '{0:get_moon(moonID)} POS "{0:get_item(typeID)}" ({0:get_percentage(shieldValue)} shield, {0:get_percentage(armorValue)} armor, {0:get_percentage(hullValue)} hull) under attack by {0:get_character(aggressorID)}'.format(Formatter(self, notification))

    def pos_fuel_alert(self, notification):
        wants = map(lambda w: '%s: %d' % (self.get_item(w['typeID']), w['quantity']), notification['wants'])

        return '{0:get_moon(moonID)} POS "{0:get_item(typeID)}" is low on fuel: {wants}'.format(Formatter(self, notification), wants=', '.join(wants))

    def station_conquered(self, notification):
        return "Station conquered from {0:get_corporation(oldOwnerID)} by {0:get_corporation(newOwnerID)} in {0:get_system(solarSystemID)}".format(Formatter(self, notification))

    def customs_office_attacked(self, notification):
        return '"{0:get_planet(planetID)}" POCO ({0:get_percentage(shieldLevel)} shields) has been attacked by {0:get_character(aggressorID)}'.format(Formatter(self, notification))

    def customs_office_reinforced(self, notification):
        return '"{0:get_planet(planetID)}" POCO has been reinforced by {0:get_character(aggressorID)} (comes out of reinforce on "{0:eve_timestamp_to_date(reinforceExitTime)}")'.format(Formatter(self, notification))

    def structure_transferred(self, notification):
        return '"{0:get_string(structureName)}" structure in {0:get_system_from_link(solarSystemLinkData)} has been transferred from {0:get_corporation_from_link(fromCorporationLinkData)} to {0:get_corporation_from_link(toCorporationLinkData)} by {0:get_character_from_link(characterLinkData)}'.format(Formatter(self, notification))

    def entosis_capture_started(self, notification):
        return 'Capturing of "{0:get_item(structureTypeID)}" in {0:get_system(solarSystemID)} has started'.format(Formatter(self, notification))

    def entosis_enabled_structure(self, notification):
        return 'Structure "{0:get_item(structureTypeID)}" in {0:get_system(solarSystemID)} has been enabled'.format(Formatter(self, notification))

    def entosis_disabled_structure(self, notification):
        return 'Structure "{0:get_item(structureTypeID)}" in {0:get_system(solarSystemID)} has been disabled'.format(Formatter(self, notification))

    def sov_structure_reinforced(self, notification):
        return 'SOV structure "{0:get_campaign_event_type(campaignEventType)}" in {0:get_system(solarSystemID)} has been reinforced, nodes will decloak "{0:eve_timestamp_to_date(decloakTime)}"'.format(Formatter(self, notification))

    def sov_structure_command_nodes_decloaked(self, notification):
        return 'Command nodes for "{0:get_campaign_event_type(campaignEventType)}" SOV structure in {0:get_system(solarSystemID)} have decloaked'.format(Formatter(self, notification))

    def sov_structure_destroyed(self, notification):
        return 'SOV structure "{0:get_item(structureTypeID)}" in {0:get_system(solarSystemID)} has been destroyed'.format(Formatter(self, notification))

    def sov_structure_freeported(self, notification):
        return 'SOV structure "{0:get_item(structureTypeID)}" in {0:get_system(solarSystemID)} has been freeported, exits freeport on "{0:eve_timestamp_to_date(freeportexittime)}"'.format(Formatter(self, notification))

    def citadel_low_fuel(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") low fuel alert in {0:get_system(solarsystemID)}'.format(Formatter(self, notification))

    def citadel_anchored(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") anchored in {0:get_system(solarsystemID)} by {0:get_corporation_from_link(ownerCorpLinkData)}'.format(Formatter(self, notification))

    def citadel_unanchoring(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") unanchoring in {0:get_system(solarsystemID)} by {0:get_corporation_from_link(ownerCorpLinkData)}'.format(Formatter(self, notification))


    def citadel_attacked(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") attacked ({0:get_percentage(shieldPercentage)} shield, {0:get_percentage(armorPercentage)} armor, {0:get_percentage(hullPercentage)} hull) in {0:get_system(solarsystemID)} by {0:get_character(charID)}'.format(Formatter(self, notification))

    def citadel_onlined(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") onlined in {0:get_system(solarsystemID)}'.format(Formatter(self, notification))

    def citadel_lost_shields(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") lost shields in {0:get_system(solarsystemID)} (comes out of reinforce on "{0:eve_duration_to_date(notification_timestamp, timeLeft)}")'.format(Formatter(self, notification))

    def citadel_lost_armor(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") lost armor in {0:get_system(solarsystemID)} (comes out of reinforce on "{0:eve_duration_to_date(notification_timestamp, timeLeft)}")'.format(Formatter(self, notification))

    def citadel_destroyed(self, notification):
        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") destroyed in {0:get_system(solarsystemID)} owned by {0:get_corporation_from_link(ownerCorpLinkData)}'.format(Formatter(self, notification))

    def citadel_out_of_fuel(self, notification):
        services = map(lambda ID: self.get_item(ID), notification['listOfServiceModuleIDs'])

        return 'Citadel ({0:get_structure_type_from_link(structureShowInfoData)}, "{0:get_structure_name(structureID)}") ran out of fuel in {0:get_system(solarsystemID)} with services "{services}"'.format(Formatter(self, notification), services=', '.join(services))

    def structure_anchoring_alert(self, notification):
        return 'New structure ({0:get_item(typeID)}) anchored in "{0:get_moon(moonID)}" by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def ihub_bill_about_to_expire(self, notification):
        return 'IHUB bill to {0:get_corporation(corpID)} for system {0:get_system(solarSystemID)} will expire {0:eve_timestamp_to_date(dueDate)}'.format(Formatter(self, notification))

    def sov_structure_self_destructed(self, notification):
        return 'SOV structure "{0:get_item(structureTypeID)}" has self destructed in {0:get_system(solarSystemID)}'.format(Formatter(self, notification))

    def sov_structure_started_self_destructing(self, notification):
        return 'Self-destruction of "{0:get_item(structureTypeID)}" SOV structure in {0:get_system(solarSystemID)} has been requested by {0:get_character(charID)}. Structure will self-destruct on "{0:eve_timestamp_to_date(destructTime)}"'.format(Formatter(self, notification))

    def moon_extraction_started(self, notification):
        return 'Moon extraction started by {0:get_character(startedBy)} in {0:get_system(solarSystemID)} ({0:get_moon(moonID)}, "{0:get_string(structureName)}") and will be ready on {0:eve_timestamp_to_date(readyTime)} (or will auto-explode into a belt on {0:eve_timestamp_to_date(autoTime)})'.format(Formatter(self, notification))

    def moon_extraction_cancelled(self, notification):
        return 'Moon extraction cancelled by {0:get_character(cancelledBy)} in {0:get_system(solarSystemID)} ({0:get_moon(moonID)}, "{0:get_string(structureName)}")'.format(Formatter(self, notification))

    def moon_extraction_finished(self, notification):
        return 'Moon extraction has finished and is ready in {0:get_system(solarSystemID)} ({0:get_moon(moonID)}, "{0:get_string(structureName)}") to be exploded into a belt (or will auto-explode into one on {0:eve_timestamp_to_date(autoTime)})'.format(Formatter(self, notification))

    def moon_extraction_turned_into_belt(self, notification):
        return 'Moon laser has been fired by {0:get_character(firedBy)} in {0:get_system(solarSystemID)} ({0:get_moon(moonID)}, "{0:get_string(structureName)}") and the belt is ready to be mined'.format(Formatter(self, notification))

    def moon_extraction_autofractured(self, notification):
        return 'Moon extraction in {0:get_system(solarSystemID)} ({0:get_moon(moonID)}, "{0:get_string(structureName)}") has autofractured into a belt and is ready to be mined'.format(Formatter(self, notification))

    def corporation_bill(self, notification):
        return 'Corporation bill issued to {0:get_corporation_or_alliance(debtorID)} by {0:get_corporation_or_alliance(creditorID)} for the amount of {0:get_isk(amount)} at {0:eve_timestamp_to_date(currentDate)}. Bill is due {0:eve_timestamp_to_date(dueDate)}'.format(Formatter(self, notification))

    def corporation_bill_paid(self, notification):
        return 'Corporation bill for {0:get_isk(amount)} was paid. Bill was due {0:eve_timestamp_to_date(dueDate)}'.format(Formatter(self, notification))

    def new_character_application_to_corp(self, notification):
        return 'Character {0:get_character(charID)} has applied to corporation {0:get_corporation(corpID)}. Application text:\n\n{0:get_string(applicationText)}'.format(Formatter(self, notification))

    def character_application_withdrawn(self, notification):
        return 'Character {0:get_character(charID)} application to corporation {0:get_corporation(corpID)} has been withdrawn'.format(Formatter(self, notification))

    def character_application_accepted(self, notification):
        return 'Character {0:get_character(charID)} accepted to corporation {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def character_left_corporation(self, notification):
        return 'Character {0:get_character(charID)} left corporation {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def new_corporation_ceo(self, notification):
        return '{0:get_character(newCeoID)} has replaced {0:get_character(oldCeoID)} as the new CEO of {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def corporation_vote_initiated(self, notification):
        return "New corporation vote for '%s':\n\n%s" % (notification['subject'], notification['body'])

    def corporation_vote_for_ceo_revoked(self, notification):
        return 'Corporation "{0:get_corporation(corpID)}" vote for new CEO has been revoked by {0:get_character(charID)}'.format(Formatter(self, notification))

    def corporation_tax_changed(self, notification):
        return 'Tax changed from {0:get_percentage(oldTaxRate)} to {0:get_percentage(newTaxRate)} for {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def corporation_dividend_paid_out(self, notification):
        return 'Corporation {0:get_corporation(corpID)} has paid out {0:get_isk(payout)} ISK in dividends'.format(Formatter(self, notification))

    def bounty_claimed(self, notification):
        return 'A bounty of {0:get_isk(amount)} has been claimed for killing {0:get_character(charID)}'.format(Formatter(self, notification))

    def kill_report_victim(self, notification):
        return 'Died in a(n) {0:get_item(victimShipTypeID)}: {0:get_killmail(killMailID, killMailHash)}'.format(Formatter(self, notification))

    def kill_report_final_blow(self, notification):
        return 'Got final blow on {0:get_item(victimShipTypeID)}: {0:get_killmail(killMailID, killMailHash)}'.format(Formatter(self, notification))

    @abc.abstractmethod
    def get_corporation(self, corporation_id):
        return

    @abc.abstractmethod
    def get_alliance(self, alliance_id):
        return

    def get_corporation_or_alliance(self, entity_id):
        try:
            return self.get_corporation(entity_id)
        except:
            return self.get_alliance(entity_id)

    def get_item(self, item_id):
        item = self.eve.get_item(item_id)
        return item['name']

    @abc.abstractmethod
    def get_system(self, system_id):
        return

    def get_planet(self, planet_id):
        planet = self.eve.get_planet(planet_id)
        system = self.get_system(planet['system_id'])
        return '%s in %s' % (planet['name'], system)

    def get_moon(self, moon_id):
        moon = self.eve.get_moon(moon_id)
        return moon['name']

    @abc.abstractmethod
    def get_character(self, character_id):
        return

    @abc.abstractmethod
    def get_killmail(self, kill_id):
        return

    def get_campaign_event_type(self, event_type):
        if event_type == 1:
            return 'TCU'
        elif event_type == 2:
            return 'IHUB'
        elif event_type == 3:
            return 'Station'
        else:
            return 'Unknown structure type "%d"' % event_type

    def get_structure_name(self, structure_id):
        structure = self.eve.get_structure(structure_id)
        if 'name' in structure:
            return structure['name']
        else:
            return "Unknown name"

    def timestamp_to_date(self, timestamp):
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')

    def eve_timestamp_to_date(self, microseconds):
        """
        Convert microsoft epoch to unix epoch
        Based on: http://www.wiki.eve-id.net/APIv2_Char_NotificationTexts_XML
        """

        seconds = microseconds/10000000 - 11644473600
        return datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

    def eve_duration_to_date(self, timestamp, microseconds):
        """
        Convert microsoft epoch to unix epoch
        Based on: http://www.wiki.eve-id.net/APIv2_Char_NotificationTexts_XML
        """

        seconds = microseconds/10000000
        timedelta = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(seconds=seconds)
        return timedelta.strftime('%Y-%m-%d %H:%M:%S')

    def get_percentage(self, value):
        if value <= 1:
            value = value * 100
        return '%.1f%%' % value

    def get_isk(self, isk):
        return '%.2f ISK' % isk

    def get_string(self, value):
        return str(value)

    def get_corporation_from_link(self, show_info):
        return self.get_corporation(show_info[-1])

    def get_structure_type_from_link(self, show_info):
        return self.get_item(show_info[1])

    def get_system_from_link(self, show_info):
        return self.get_system(show_info[-1])

    def get_character_from_link(self, show_info):
        return self.get_character(show_info[-1])
