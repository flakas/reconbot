Reconbot for Eve Online [![CircleCI](https://circleci.com/gh/flakas/reconbot.svg?style=svg)](https://circleci.com/gh/flakas/reconbot)
=======================

Reconbot is a notification relay bot for an MMO game [Eve Online](http://secure.eveonline.com/signup/?invc=905e73a0-eb57-49ab-8fe5-9759c2ba5e99&action=buddy).
It fetches character notifications from the EVE API, filters irrelevant ones out and sends relevant ones to set Slack or Discord channels.
Notifications like SOV changes, SOV/POS/POCO/Citadel attacks.

# Setup

Reconbot was intended to be used as a base for further customizations, or integration with other systems, but it can be run via `run.py` as well. Check it out for an example.

## 1. EVE Developer Application

This tool is ready to be used with [Eve's ESI API](https://esi.tech.ccp.is/). You will need to register your application on [EVE Developers page](https://developers.eveonline.com/applications).

When registering your EVE Application, please pick `Authentication & API Access` connection type, and make sure your application requests these permissions:

- `esi-universe.read_structures.v1` - necessary to fetch names of any linked structures;
- `esi-characters.read_notifications.v1` - necessary to fetch character level notifications.

Take note of the `Client ID` and `Secret Key`, as they are necessary for establishing communication with ESI API.

## 2. Slack or Discord chat tools

To add a Slack integration, check out [this Slack documentation page on Bot Users](https://api.slack.com/bot-users) (or [create bot user for your workspace](https://my.slack.com/services/new/bot)). Take note of the API token.

To add a Discord integration, check out [this Discord documentation page on Bot accounts](https://discordapp.com/developers/docs/topics/oauth2#bots).
You will need to [create an application](https://discordapp.com/developers/applications/me#top) and add it to your discord server.
See [this guide](https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord) for more visual step-by-step instructions.
You will need a `Token` for your Bot User, and `Channel ID` where to post messages in.

## 3. Reconbot setup

1. Clone this repository
2. Execute `download_dump.sh`, which will download the latest Static Data Export from [Fuzzwork Enterprises](https://www.fuzzwork.co.uk/) and will store it in the current directory
3. Modify `run.py` with your EVE API keys, key groups and Slack/Discord accounts/channels.
  `whitelist` will contain notification types you're interested in, and `characters` should contain entries for API keys of individual characters.
4. Install Python dependencies with `pip install -r requirements.txt`
5. Execute `python run.py` and wait for notifications to arrive!

# Other notes

Reconbot by default will try to evenly spread out checking API keys over the cache expiry window (which is 10 minutes for ESI), meaning that with 2 API keys in rotation an API key will be checked every ~5 minutes (with 10 keys - every minute), which can be useful to detect alliance or corporation-wide notifications more frequently than only once every 10 minutes.

## Supported notifications

As of writing this tool there is little documentation about the types of notifications available and their contents. The following list has been assembled from working experience, is not fully complete and may be subject to change as CCP changes internals:

- AllWarDeclaredMsg
- DeclareWar
- AllWarInvalidatedMsg
- AllyJoinedWarAggressorMsg
- CorpWarDeclaredMsg
- EntosisCaptureStarted
- SovCommandNodeEventStarted
- SovStructureDestroyed
- SovStructureReinforced
- StructureUnderAttack
- OwnershipTransferred
- StructureOnline
- StructureDestroyed
- StructureFuelAlert
- StructureAnchoring
- StructureUnanchoring
- StructureServicesOffline
- StructureLostShields
- StructureLostArmor
- TowerAlertMsg
- TowerResourceAlertMsg
- StationServiceEnabled
- StationServiceDisabled
- OrbitalReinforced
- OrbitalAttacked
- SovAllClaimAquiredMsg
- SovStationEnteredFreeport
- AllAnchoringMsg
- InfrastructureHubBillAboutToExpire
- SovAllClaimLostMsg
- SovStructureSelfDestructRequested
- SovStructureSelfDestructFinished
- StationConquerMsg
- notificationTypeMoonminingExtractionStarted
- MoonminingExtractionFinished
- MoonminingLaserFired
- MoonminingAutomaticFracture
- CorpAllBillMsg
- BillPaidCorpAllMsg
- CharAppAcceptMsg
- CorpAppNewMsg
- CharAppWithdrawMsg
- CharLeftCorpMsg
- CorpNewCEOMsg
- CorpVoteMsg
- CorpVoteCEORevokedMsg
- CorpTaxChangeMsg
- CorpDividendMsg
- BountyClaimMsg
- KillReportVictim
- KillReportFinalBlow

Do you have sample contents of currently unsupported notification types? Consider sharing them by creating an issue, or submit a Pull Request. Any help would be appreciated!
