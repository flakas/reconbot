from queue import Queue

class ApiQueue:
    """A pool of EVE API keys to be iterated over in a sequential indefinite cycle"""

    def __init__(self, apis=[]):
        self.queue = Queue()

        if type(apis) is not list:
            raise TypeError("ApiQueue can be initialized with a list of APIs")

        if len(apis) > 0:
            for api in apis:
                self.queue.put(api)

    def add(self, api):
        self.queue.put(api)

    def get(self):
        api = self.queue.get()
        self.queue.put(api)
        return api
