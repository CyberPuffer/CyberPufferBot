# -*- coding: utf-8 -*-
from os import environ
from utils.webhook import webhook
from werkzeug.wrappers import Request
from werkzeug.test import create_environ
from json import dumps
import unittest


class Test_WebHook(unittest.TestCase):
    def test_keyword_reply(self):
        update = {
            "update_id": 400000000,
            "message": {
                "message_id": 1000,
                "from": {
                    "id": 100000000,
                    "is_bot": False,
                    "first_name": "Test",
                    "last_name": "User",
                    "language_code": "zh-hans"
                    },
                "chat": {
                    "id": 200000000,
                    "first_name": "Test",
                    "last_name": "User",
                    "type": "private"
                    },
                "date": 2000000000,
                "text": "test"
                }
            }
        environ = create_environ(
            method='POST',
            data=dumps(update)
        )
        request = Request(environ)
        result = webhook(request)
        self.assertEqual(result, 'ok')
