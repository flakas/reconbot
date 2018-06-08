class FilterNotifier:
    """ Filters notifications based on their type or keywords """
    def __init__(self, notifier, keywords=[], ignore=[]):
        self.notifier = notifier
        self.keywords = keywords
        self.ignore = ignore

    def notify(self, text, options={}):
        if len(self.ignore) > 0 and any(keyword in text for keyword in self.ignore):
            return False

        if len(self.keywords) == 0 or any(keyword in text for keyword in self.keywords):
            self.notifier.notify(text, options)
