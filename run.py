import schedule
import time
import sqlite3

from reconbot.tasks import esi_notification_task
from reconbot.notifiers.caching import CachingNotifier
from reconbot.notifiers.slack import SlackNotifier
from reconbot.notifiers.discord import DiscordNotifier
from reconbot.notifiers.discordwebhook import DiscordWebhookNotifier
from reconbot.notifiers.splitter import SplitterNotifier
from reconbot.notifiers.filter import FilterNotifier
from reconbot.apiqueue import ApiQueue
from reconbot.esi import ESI
from reconbot.sso import SSO

# Configuration

db_file = 'datadump/sqlite-latest.sqlite'

# ESI notification endpoint cache timer in minutes
notification_caching_timer = 10

# Slack bot integration API key
slack_apis = {
  'example': {
    'api_key': 'xxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx',
    'username': 'reconbot',
  },
}

# Discord bot integration API key and channel
discord = {
    'personal': {
        'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'channel_id': 'xxxxxxxxxxxxxxxxxx'
    },
    'my-webhook': {
        'url': 'https://discordapp.com/api/webhooks/xxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
}

# Eve online SSO application Client ID and Secret Key, used to get access
# tokens for ESI API. Get them on:
# https://developers.eveonline.com/applications
sso_app = {
    'client_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'secret_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
}

# A dictionary of API key groups.
# Get refresh tokens for your characters by following Fuzzwork's guide:
# https://www.fuzzwork.co.uk/2017/03/14/using-esi-google-sheets/
eve_apis = {
    'fc-team': {
        'notifications': {
            'whitelist': None, # allow all notification types
        },
        'characters': {
            'ccp-example-1': {
                'character_name': 'CCP Example',
                'character_id': 11111111,
                'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
            'ccp-example-2': {
                'character_name': 'CCP Example 2',
                'character_id': 33333333,
                'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
        },
    },
    'logistics-team': {
        'notifications': {
            'whitelist': [ # Allow only specified notification types
                'SovStructureDestroyed',
                'SovStructureReinforced',
                'StructureUnderAttack',
                'OwnershipTransferred',
                'StructureOnline',
                'StructureFuelAlert',
                'StructureAnchoring',
                'StructureServicesOffline',
                'StructureLostShields',
                'StructureLostArmor',
                'TowerAlertMsg',
                'StationServiceEnabled',
                'StationServiceDisabled',
                'OrbitalReinforced',
                'OrbitalAttacked',
                'SovAllClaimAquiredMsg',
                'SovStationEnteredFreeport',
                'SovAllClaimLostMsg',
                'SovStructureSelfDestructRequested',
                'SovStructureSelfDestructFinished',
                'StationConquerMsg',
                'notificationTypeMoonminingExtractionStarted',
                'MoonminingExtractionFinished',
                'MoonminingLaserFired',
            ],
        },
        'characters': {
            'ccp-example-3': {
                'character_name': 'CCP Example 3',
                'character_id': 55555555,
                'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
            'ccp-example-4': {
                'character_name': 'CCP Example 4',
                'character_id': 77777777,
                'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            },
        },
    }
}

def api_to_sso(api):
    return SSO(
        sso_app['client_id'],
        sso_app['secret_key'],
        api['refresh_token'],
        api['character_id']
    )

api_queue_fc = ApiQueue(list(map(api_to_sso, eve_apis['fc-team']['characters'].values())))
api_queue_logistics = ApiQueue(list(map(api_to_sso, eve_apis['logistics-team']['characters'].values())))

db_connection = sqlite3.connect(db_file)
db_connection.row_factory = sqlite3.Row
db = db_connection.cursor()

def notifications_job_fc():
    esi_notification_task(
        eve_apis['fc-team']['notifications'],
        api_queue_fc,
        'slack',
        CachingNotifier(
            SplitterNotifier([
                SlackNotifier(
                    slack_apis['example']['api_key'],
                    slack_apis['example']['username'],
                    '#fc',
                    'online'
                ),
                SlackNotifier(
                    slack_apis['example']['api_key'],
                    slack_apis['example']['username'],
                    '#logistics',
                    'all'
                )
            ]),
            duration=3600
        )
    )

def notifications_job_logistics():
    esi_notification_task(
        eve_apis['logistics-team']['notifications'],
        api_queue_logistics,
        'discord',
        CachingNotifier(
            SplitterNotifier([
                DiscordNotifier(
                    discord['personal']['token'],
                    discord['personal']['channel_id']
                ),
                DiscordWebhookNotifier(
                    discord['my-webhook']['url']
                )
            ]),
            duration=3600
        )
    )


def run_and_schedule(characters, notifications_job):
    """
    Runs a job immediately to avoid having to wait for the delay to end,
    and schedules the job to be run continuously.
    """
    notifications_job()
    schedule.every(notification_caching_timer/len(characters)).minutes.do(notifications_job)

run_and_schedule(eve_apis['fc-team']['characters'], notifications_job_fc)
run_and_schedule(eve_apis['logistics-team']['characters'], notifications_job_logistics)

while True:
    schedule.run_pending()
    time.sleep(1)
