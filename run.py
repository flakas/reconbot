import schedule
import time
import sqlite3

from reconbot.tasks import notification_task
from reconbot.notifiers.caching import CachingNotifier
from reconbot.notifiers.slack import SlackNotifier
from reconbot.notifiers.splitter import SplitterNotifier
from reconbot.apiqueue import ApiQueue

db_file = 'datadump/sqlite-latest.sqlite'

slack_apis = {
  'example': {
    'api_key': 'xxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx',
    'username': 'reconbot',
  },
}

eve_apis = {
    'example-group': {
        'notifications': {
            'whitelist': [75, 93, 94, 95, 147, 148, 149, 160, 161, 162, 163, 181, 182, 184, 185, 188, 198],
        },
        'characters': {
            'ccp-example-1': {
                'character_name': 'CCP Example',
                'character_id': 11111111,
                'key_id': 2222222,
                'vcode': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            },
            'ccp-example-2': {
                'character_name': 'CCP Example 2',
                'character_id': 33333333,
                'key_id': 4444444,
                'vcode': 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',
            },
        },
    }
}

api_queue = ApiQueue(list(eve_apis['example-group']['characters'].values()))

db_connection = sqlite3.connect(db_file)
db_connection.row_factory = sqlite3.Row
db = db_connection.cursor()

def notifications_job():
    notification_task(
        db,
        eve_apis['example-group']['notifications'],
        api_queue,
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
                    '#recon',
                    'all'
                )
            ]),
            duration=3600
        )
    )

schedule.every(31/len(eve_apis['example-group']['characters'])).minutes.do(notifications_job)

while True:
    schedule.run_pending()
    time.sleep(1)
