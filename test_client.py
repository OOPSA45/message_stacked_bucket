import client
import unittest



class TestPresenceFormat(unittest.TestCase):

    def test_presence_format(self):
        func = client.presence_format('presence', 'any_timestamp')
        self.assertEqual(func, '{"action": "presence", "time": "any_timestamp"}')

    # def test_response_parse(self):
    #     response = {
    #         "response": "200",
    #         "alert": "test_message"
    #     }
    #     self.assertEqual(client.response_parse(response), [str])


unittest.TestCase()