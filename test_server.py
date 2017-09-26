import server
import unittest

class TestResponseFormat(unittest.TestCase):

    def test_response_format(self):
        func = server.presence_format('200', 'any_time', 'any_text')
        self.assertEqual(func, '{"response": "200", "alert": "any_text", "time": "any_timestamp"}')

unittest.TestCase()