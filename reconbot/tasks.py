import sys, traceback

import evelink.api
import evelink.char
import evelink.eve

from reconbot.eve import Eve
from reconbot.notificationprinters.slack import Slack
from reconbot.notificationprinters.slack import Discord

def notification_task(db, notification_options, api_queue, printer, notifier):
    MAX_NOTIFICATION_AGE_IN_SECONDS = 3600

    try:
        character_api = api_queue.get()

        game_api = evelink.eve.EVE()
        character_api = evelink.char.Char(
            char_id=character_api['character_id'],
            api=evelink.api.API(
                api_key=(character_api['key_id'], character_api['vcode'])))

        eve = Eve(db, game_api, character_api)

        notifications = eve.get_notifications(max_age=MAX_NOTIFICATION_AGE_IN_SECONDS)

        if notification_options['whitelist']:
            notifications = [notification for notification in notifications if notification['notification_type'] in notification_options['whitelist']]

        if printer == 'discord':
            printer = Discord(eve)
        else:
            printer = Slack(eve)

        messages = map(lambda text: printer.transform(text), notifications)

        for message in messages:
            notifier.notify(message)

    except Exception as e:
        print('Exception in notification task')
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print(e)
        print('-' * 60)
