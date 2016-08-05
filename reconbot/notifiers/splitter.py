class SplitterNotifier:
    def __init__(self, notifiers=[]):
        self.notifiers = notifiers

    def notify(self, text, options={}):
        for notifier in self.notifiers:
            notifier.notify(text, options)
