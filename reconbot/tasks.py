import sys, traceback, datetime

from reconbot.notificationprinters.esi.slack import Slack as ESISlack
from reconbot.notificationprinters.esi.discord import Discord as ESIDiscord
from reconbot.esi import ESI

def esi_notification_task(notification_options, api_queue, printer, notifier):
    MAX_NOTIFICATION_AGE_IN_SECONDS = 3600

    try:
        sso = api_queue.get()

        esi = ESI(sso)

        notifications = esi.get_new_notifications(max_age=MAX_NOTIFICATION_AGE_IN_SECONDS)

        if 'whitelist' in notification_options and type(notification_options['whitelist']) == 'list':
            notifications = [notification for notification in notifications if notification['type'] in notification_options['whitelist']]

        if printer == 'discord':
            printer = ESIDiscord(esi)
        else:
            printer = ESISlack(esi)

        messages = map(lambda text: printer.transform(text), notifications)

        for message in messages:
            notifier.notify(message)

    except Exception as e:
        notify_exception("esi_notification_task", e)

def notify_exception(location, exception):
    print('[%s] Exception in %s' % (datetime.datetime.now(), location))
    print('-' * 60)
    traceback.print_exc(file=sys.stdout)
    print(exception)
    print('-' * 60)
