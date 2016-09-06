import time

class CachingNotifier:
    """ Caches notifications to ensure duplicates don't pass through """

    def __init__(self, notifier, duration=3600):
        self.duration = duration
        self.notifier = notifier
        self.cache = {}

    def notify(self, text, options={}):
        if not self._is_cached(text):
            self._cache(text)
            self.notifier.notify(text, options)

        self._cleanup()

    def _cache(self, message):
        self.cache[message] = time.time() + self.duration

    def _is_cached(self, message):
        return message in self.cache and self.cache[message] > time.time()

    def _cleanup(self):
        current_time = time.time()
        for message, timeout in self.cache.items():
            if timeout < current_time:
                del self.cache[message]

