import abc
import datetime
import yaml

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
        owner = self.get_corporation(notification['corpID'])
        system = self.get_system(notification['solarSystemID'])

        return 'SOV lost in %s by %s' % (system, owner)

    def sov_claim_acquired(self, notification):
        owner = self.get_corporation(notification['corpID'])
        system = self.get_system(notification['solarSystemID'])

        return 'SOV acquired in %s by %s' % (system, owner)

    def pos_anchoring_alert(self, notification):
        owner = self.get_corporation(notification['corpID'])
        moon = self.eve.get_moon(notification['moonID'])

        return 'New POS anchored in "%s" by %s' % (moon['name'], owner)

    def pos_attack(self, notification):
        moon = self.eve.get_moon(notification['moonID'])
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

    def pos_fuel_alert(self, notification):
        moon = self.eve.get_moon(notification['moonID'])
        item_type = self.get_item(notification['typeID'])
        wants = map(lambda w: '%s: %d' % (self.get_item(w['typeID']), w['quantity']), notification['wants'])

        return "%s POS \"%s\" is low on fuel: %s" % (
            moon['name'],
            item_type,
            ', '.join(wants)
        )

    def station_conquered(self, notification):
        system = self.get_system(notification['solarSystemID'])
        old_owner = self.get_corporation(notification['oldOwnerID'])
        new_owner = self.get_corporation(notification['newOwnerID'])

        return "Station conquered from %s by %s in %s" % (old_owner, new_owner, system)

    def customs_office_attacked(self, notification):
        attacker = self.get_character(notification['aggressorID'])
        planet = self.get_planet(notification['planetID'])
        shields = int(notification['shieldLevel']*100)

        return "\"%s\" POCO (%d%% shields) has been attacked by %s" % (planet, shields, attacker)

    def customs_office_reinforced(self, notification):
        attacker = self.get_character(notification['aggressorID'])
        planet = self.get_planet(notification['planetID'])
        timestamp = self.eve_timestamp_to_date(notification['reinforceExitTime'])

        return "\"%s\" POCO has been reinforced by %s (comes out of reinforce on \"%s\")" % (planet, attacker, timestamp)

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
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Capturing of \"%s\" in %s has started" % (structure, system)

    def entosis_enabled_structure(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Structure \"%s\" in %s has been enabled" % (structure, system)

    def entosis_disabled_structure(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return "Structure \"%s\" in %s has been disabled" % (structure, system)

    def sov_structure_reinforced(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure_type = self.get_campaign_event_type(notification['campaignEventType'])
        timestamp = self.eve_timestamp_to_date(notification['decloakTime'])

        return "SOV structure \"%s\" in %s has been reinforced, nodes will decloak \"%s\"" % (structure_type, system, timestamp)

    def sov_structure_command_nodes_decloaked(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure_type = self.get_campaign_event_type(notification['campaignEventType'])

        return "Command nodes for \"%s\" SOV structure in %s have decloaked" % (structure_type, system)

    def sov_structure_destroyed(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure_type = self.get_item(notification['structureTypeID'])

        return "SOV structure \"%s\" in %s has been destroyed" % (structure_type, system)

    def sov_structure_freeported(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure_type = self.get_item(notification['structureTypeID'])
        timestamp = self.eve_timestamp_to_date(notification['freeportexittime'])

        return "SOV structure \"%s\" in %s has been freeported, exits freeport on \"%s\"" % (structure_type, system, timestamp)

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
        owner = self.get_corporation(notification['corpID'])
        moon = self.eve.get_moon(notification['moonID'])
        item_type = self.get_item(notification['typeID'])

        return 'New structure (%s) anchored in "%s" by %s' % (item_type, moon['name'], owner)

    def ihub_bill_about_to_expire(self, notification):
        corp = self.get_corporation(notification['corpID'])
        due_date = self.eve_timestamp_to_date(notification['dueDate'])
        system = self.get_system(notification['solarSystemID'])

        return 'IHUB bill to %s for system %s will expire %s' % (corp, system, due_date)

    def sov_structure_self_destructed(self, notification):
        system = self.get_system(notification['solarSystemID'])
        structure = self.get_item(notification['structureTypeID'])

        return 'SOV structure "%s" has self destructed in %s' % (structure, system)

    def sov_structure_started_self_destructing(self, notification):
        character = self.get_character(notification['charID'])
        end_time = self.eve_timestamp_to_date(notification['destructTime'])
        system = self.get_system(notification['solarSystemID'])
        item = self.get_item(notification['structureTypeID'])

        return 'Self-destruction of "%s" SOV structure in %s has been requested by %s. Structure will self-destruct on "%s"' % (item, system, character, end_time)

    def moon_extraction_started(self, notification):
        started_by = self.get_character(notification['startedBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.eve.get_moon(notification['moonID'])
        ready_time = self.eve_timestamp_to_date(notification['readyTime'])
        auto_destruct_time = self.eve_timestamp_to_date(notification['autoTime'])
        structure_name = notification['structureName']

        return 'Moon extraction started by %s in %s (%s, "%s") and will be ready on %s (or will auto-explode into a belt on %s)' % (started_by, system, moon['name'], structure_name, ready_time, auto_destruct_time)

    def moon_extraction_cancelled(self, notification):
        cancelled_by = self.get_character(notification['cancelledBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.eve.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon extraction cancelled by %s in %s (%s, "%s")' % (cancelled_by, system, moon['name'], structure_name)

    def moon_extraction_finished(self, notification):
        system = self.get_system(notification['solarSystemID'])
        moon = self.eve.get_moon(notification['moonID'])
        auto_destruct_time = self.eve_timestamp_to_date(notification['autoTime'])
        structure_name = notification['structureName']

        return 'Moon extraction has finished and is ready in %s (%s, "%s") to be exploded into a belt (or will auto-explode into one on %s)' % (system, moon['name'], structure_name, auto_destruct_time)

    def moon_extraction_turned_into_belt(self, notification):
        fired_by = self.get_character(notification['firedBy'])
        system = self.get_system(notification['solarSystemID'])
        moon = self.eve.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon laser has been fired by %s in %s (%s, "%s") and the belt is ready to be mined' % (fired_by, system, moon['name'], structure_name)

    def moon_extraction_autofractured(self, notification):
        system = self.get_system(notification['solarSystemID'])
        moon = self.eve.get_moon(notification['moonID'])
        structure_name = notification['structureName']

        return 'Moon extraction in %s (%s, "%s") has autofractured into a belt and is ready to be mined' % (system, moon['name'], structure_name)

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
        character = self.get_character(notification['charID'])
        corporation = self.get_corporation(notification['corpID'])

        return 'Character %s application to corporation %s has been withdrawn' % (character, corporation)

    def character_application_accepted(self, notification):
        character = self.get_character(notification['charID'])
        corporation = self.get_corporation(notification['corpID'])

        return 'Character %s accepted to corporation %s' % (character, corporation)

    def character_left_corporation(self, notification):
        character = self.get_character(notification['charID'])
        corporation = self.get_corporation(notification['corpID'])

        return 'Character %s left corporation %s' % (character, corporation)

    def new_corporation_ceo(self, notification):
        old_ceo = self.get_character(notification['oldCeoID'])
        new_ceo = self.get_character(notification['newCeoID'])
        corporation = self.get_corporation(notification['corpID'])

        return '%s has replaced %s as the new CEO of %s' % (new_ceo, old_ceo, corporation)

    def corporation_vote_initiated(self, notification):
        return "New corporation vote for '%s':\n\n%s" % (notification['subject'], notification['body'])

    def corporation_vote_for_ceo_revoked(self, notification):
        character = self.get_character(notification['charID'])
        corporation = self.get_corporation(notification['corpID'])

        return 'Corporation "%s" vote for new CEO has been revoked by %s' % (corporation, character)

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

