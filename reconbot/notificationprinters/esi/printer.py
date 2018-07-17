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
        # May contain corporation or alliance IDs
        try:
            against_corp = self.get_corporation(notification['againstID'])
        except:
            against_corp = self.get_alliance(notification['againstID'])
        try:
            declared_by_corp = self.get_corporation(notification['declaredByID'])
        except:
            declared_by_corp = self.get_alliance(notification['declaredByID'])

        return 'War has been declared to %s by %s' % (against_corp, declared_by_corp)

    def declare_war(self, notification):
        character = self.get_character(notification['charID'])
        # May contain corporation or alliance IDs
        try:
            defender = self.get_corporation(notification['defenderID'])
        except:
            defender = self.get_alliance(notification['defenderID'])
        try:
            entity = self.get_corporation(notification['entityID'])
        except:
            entity = self.get_alliance(notification['entityID'])

        return '%s from %s has declared war to %s' % (character, entity, defender)


    def corporation_war_invalidated(self, notification):
        # May contain corporation or alliance IDs
        try:
            against_corp = self.get_corporation(notification['againstID'])
        except:
            against_corp = self.get_alliance(notification['againstID'])
        try:
            declared_by_corp = self.get_corporation(notification['declaredByID'])
        except:
            declared_by_corp = self.get_alliance(notification['declaredByID'])

        return 'War has been invalidated to %s by %s' % (against_corp, declared_by_corp)

    def aggressor_ally_joined_war(self, notification):
        # May contain corporation or alliance IDs
        try:
            defender = self.get_corporation(notification['defenderID'])
        except:
            defender = self.get_alliance(notification['defenderID'])
        try:
            ally = self.get_corporation(notification['allyID'])
        except:
            ally = self.get_alliance(notification['allyID'])

        timestamp = self.eve_timestamp_to_date(notification['startTime'])

        return 'Ally %s joined the war to help %s starting %s' % (ally, defender, timestamp)

    def sov_claim_lost(self, notification):
        return 'SOV lost in {0:get_system(solarSystemID)} by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def sov_claim_acquired(self, notification):
        return 'SOV acquired in {0:get_system(solarSystemID)} by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def pos_anchoring_alert(self, notification):
        return 'New POS anchored in "{0:get_moon(moonID)}" by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def pos_attack(self, notification):
        moon = self.get_moon(notification['moonID'])
        attacker = self.get_character(notification['aggressorID'])
        item_type = self.get_item(notification['typeID'])

        return "%s POS \"%s\" (%.1f%% shield, %.1f%% armor, %.1f%% hull) under attack by %s" % (
            moon,
            item_type,
            notification['shieldValue']*100,
            notification['armorValue']*100,
            notification['hullValue']*100,
            attacker
        )

    def pos_fuel_alert(self, notification):
        moon = self.get_moon(notification['moonID'])
        item_type = self.get_item(notification['typeID'])
        wants = map(lambda w: '%s: %d' % (self.get_item(w['typeID']), w['quantity']), notification['wants'])

        return "%s POS \"%s\" is low on fuel: %s" % (
            moon,
            item_type,
            ', '.join(wants)
        )

    def station_conquered(self, notification):
        return "Station conquered from {0:get_corporation(oldOwnerID)} by {0:get_corporation(newOwnerID)} in {0:get_system(solarSystemID)}".format(Formatter(self, notification))

    def customs_office_attacked(self, notification):
        attacker = self.get_character(notification['aggressorID'])
        planet = self.get_planet(notification['planetID'])
        shields = int(notification['shieldLevel']*100)

        return "\"%s\" POCO (%d%% shields) has been attacked by %s" % (planet, shields, attacker)

    def customs_office_reinforced(self, notification):
        return '"{0:get_planet(planetID)}" POCO has been reinforced by {0:get_character(aggressorID)} (comes out of reinforce on "{0:eve_timestamp_to_date(reinforceExitTime)}")'.format(Formatter(self, notification))

    def structure_transferred(self, notification):
        from_corporation = self.get_corporation(notification['fromCorporationLinkData'][-1])
        to_corporation = self.get_corporation(notification['toCorporationLinkData'][-1])
        structure = notification['structureName']
        system = self.get_system(notification['solarSystemLinkData'][-1])
        character = self.get_character(notification['characterLinkData'][-1])

        return "\"%s\" structure in %s has been transferred from %s to %s by %s" % (
            structure,
            system,
            from_corporation,
            to_corporation,
            character
        )

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
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") low fuel alert in %s" % (
            citadel_type,
            citadel_name,
            system)

    def citadel_anchored(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        corp = self.get_corporation(notification['ownerCorpLinkData'][-1])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") anchored in %s by %s" % (
            citadel_type,
            citadel_name,
            system,
            corp)

    def citadel_unanchoring(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        corp = self.get_corporation(notification['ownerCorpLinkData'][-1])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") unanchoring in %s by %s" % (
            citadel_type,
            citadel_name,
            system,
            corp)


    def citadel_attacked(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        attacker = self.get_character(notification['charID'])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") attacked (%.1f%% shield, %.1f%% armor, %.1f%% hull) in %s by %s" % (
            citadel_type,
            citadel_name,
            notification['shieldPercentage'],
            notification['armorPercentage'],
            notification['hullPercentage'],
            system,
            attacker)

    def citadel_onlined(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") onlined in %s" % (
            citadel_type,
            citadel_name,
            system)

    def citadel_lost_shields(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        citadel_name = self.get_structure_name(notification['structureID'])
        timestamp = self.eve_duration_to_date(notification['notification_timestamp'], notification['timeLeft'])

        return "Citadel (%s, \"%s\") lost shields in %s (comes out of reinforce on \"%s\")" % (
            citadel_type,
            citadel_name,
            system,
            timestamp)

    def citadel_lost_armor(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        citadel_name = self.get_structure_name(notification['structureID'])
        timestamp = self.eve_duration_to_date(notification['notification_timestamp'], notification['timeLeft'])

        return "Citadel (%s, \"%s\") lost armor in %s (comes out of reinforce on \"%s\")" % (
            citadel_type,
            citadel_name,
            system,
            timestamp)

    def citadel_destroyed(self, notification):
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        system = self.get_system(notification['solarsystemID'])
        corp = self.get_corporation(notification['ownerCorpLinkData'][-1])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") destroyed in %s owned by %s" % (
            citadel_type,
            citadel_name,
            system,
            corp)

    def citadel_out_of_fuel(self, notification):
        system = self.get_system(notification['solarsystemID'])
        citadel_type = self.get_item(notification['structureShowInfoData'][1])
        services = map(lambda ID: self.get_item(ID), notification['listOfServiceModuleIDs'])
        citadel_name = self.get_structure_name(notification['structureID'])

        return "Citadel (%s, \"%s\") ran out of fuel in %s with services \"%s\"" % (
            citadel_type,
            citadel_name,
            system,
            ', '.join(services))

    def structure_anchoring_alert(self, notification):
        return 'New structure ({0:get_item(typeID)}) anchored in "{0:get_moon(moonID)}" by {0:get_corporation(corpID)}'.format(Formatter(self, notification))

    def ihub_bill_about_to_expire(self, notification):
        return 'IHUB bill to {0:get_corporation(corpID)} for system {0:get_system(solarSystemID)} will expire {0:eve_timestamp_to_date(dueDate)}'.format(Formatter(self, notification))

    def sov_structure_self_destructed(self, notification):
        return 'SOV structure "{0:get_item(structureTypeID)}" has self destructed in {0:get_system(solarSystemID)}'.format(Formatter(self, notification))

    def sov_structure_started_self_destructing(self, notification):
        return 'Self-destruction of "{0:get_item(structureTypeID)}" SOV structure in {0:get_system(solarSystemID)} has been requested by {0:get_character(charID)}. Structure will self-destruct on "{0:eve_timestamp_to_date(destructTime)}"'.format(Formatter(self, notification))

    def moon_extraction_started(self, notification):
        started_by = self.get_character(notification['startedBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.get_moon(notification['moonID'])
        ready_time = self.eve_timestamp_to_date(notification['readyTime'])
        auto_destruct_time = self.eve_timestamp_to_date(notification['autoTime'])
        structure_name = notification['structureName']

        return 'Moon extraction started by %s in %s (%s, "%s") and will be ready on %s (or will auto-explode into a belt on %s)' % (started_by, system, moon, structure_name, ready_time, auto_destruct_time)

    def moon_extraction_cancelled(self, notification):
        cancelled_by = self.get_character(notification['cancelledBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon extraction cancelled by %s in %s (%s, "%s")' % (cancelled_by, system, moon, structure_name)

    def moon_extraction_finished(self, notification):
        system = self.get_system(notification['solarSystemID'])
        moon = self.get_moon(notification['moonID'])
        auto_destruct_time = self.eve_timestamp_to_date(notification['autoTime'])
        structure_name = notification['structureName']

        return 'Moon extraction has finished and is ready in %s (%s, "%s") to be exploded into a belt (or will auto-explode into one on %s)' % (system, moon, structure_name, auto_destruct_time)

    def moon_extraction_turned_into_belt(self, notification):
        fired_by = self.get_character(notification['firedBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon laser has been fired by %s in %s (%s, "%s") and the belt is ready to be mined' % (fired_by, system, moon, structure_name)

    def moon_extraction_autofractured(self, notification):
        system = self.get_system(notification['solarSystemID'])
        moon = self.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon extraction in %s (%s, "%s") has autofractured into a belt and is ready to be mined' % (system, moon, structure_name)

    def corporation_bill(self, notification):
        try:
            debtor = self.get_corporation(notification['debtorID'])
        except:
            debtor = self.get_alliance(notification['debtorID'])
        try:
            creditor = self.get_corporation(notification['creditorID'])
        except:
            creditor = self.get_alliance(notification['creditorID'])
        current_timestamp = self.eve_timestamp_to_date(notification['currentDate'])
        due_timestamp = self.eve_timestamp_to_date(notification['dueDate'])

        return 'Corporation bill issued to %s by %s for the amount of %.2f ISK at %s. Bill is due %s' % (
            debtor,
            creditor,
            notification['amount'],
            current_timestamp,
            due_timestamp
        )

    def corporation_bill_paid(self, notification):
        due_timestamp = self.eve_timestamp_to_date(notification['dueDate'])

        return 'Corporation bill for %.2f ISK was paid. Bill was due %s' % (
            notification['amount'],
            due_timestamp
        )

    def new_character_application_to_corp(self, notification):
        character = self.get_character(notification['charID'])
        corporation = self.get_corporation(notification['corpID'])

        return "Character %s has applied to corporation %s. Application text:\n\n%s" % (character, corporation, notification['applicationText'])

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
        corporation = self.get_corporation(notification['corpID'])

        return 'Tax changed from %.1f%% to %.1f%% for %s' % (notification['oldTaxRate'], notification['newTaxRate'], corporation)

    def corporation_dividend_paid_out(self, notification):
        corporation = self.get_corporation(notification['corpID'])

        return 'Corporation %s has paid out %.2f ISK in dividends' % (corporation, notification['payout'])

    def bounty_claimed(self, notification):
        character = self.get_character(notification['charID'])
        amount = notification['amount']

        return 'A bounty of %.2f ISK has been claimed for killing %s' % (amount, character)

    def kill_report_victim(self, notification):
        kill_mail = self.get_killmail(
            notification['killMailID'],
            notification['killMailHash']
        )
        victim_ship_type = self.get_item(notification['victimShipTypeID'])

        return 'Died in a(n) %s: %s' % (victim_ship_type, kill_mail)

    def kill_report_final_blow(self, notification):
        kill_mail = self.get_killmail(
            notification['killMailID'],
            notification['killMailHash']
        )
        victim_ship_type = self.get_item(notification['victimShipTypeID'])

        return 'Got final blow on %s: %s' % (victim_ship_type, kill_mail)

    @abc.abstractmethod
    def get_corporation(self, corporation_id):
        return

    @abc.abstractmethod
    def get_alliance(self, alliance_id):
        return

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

