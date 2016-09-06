from unittest import TestCase
from unittest.mock import Mock
from reconbot.apiqueue import ApiQueue

class ApiQueueTest(TestCase):
    def test_api_keys_can_be_added(self):
        queue = ApiQueue()
        queue.add("my api key")

        self.assertEqual("my api key", queue.get())

    def test_can_be_initialized_with_api_keys(self):
        queue = ApiQueue(["first key", "second key"])

        self.assertEqual("first key", queue.get())
        self.assertEqual("second key", queue.get())

    def test_api_keys_are_used_cyclically(self):
        queue = ApiQueue(["first key", "second key"])

        self.assertEqual("first key", queue.get())
        self.assertEqual("second key", queue.get())
        self.assertEqual("first key", queue.get())
        self.assertEqual("second key", queue.get())

    def test_it_raises_exception_if_initialized_not_with_list(self):
        with self.assertRaises(TypeError):
            ApiQueue({'key': 'value'})
