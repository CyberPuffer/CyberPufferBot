# -*- coding: utf-8 -*-
from os import environ
from main import webhook
from utils import config
from werkzeug.wrappers import Request
from werkzeug.test import create_environ
from json import dumps
import unittest


class Test_WebHook(unittest.TestCase):
    def test_keyword_reply(self):
        test_user = int(config.test_user_id)
        update = {
            "update_id": 400000000,
            "message": {
                "message_id": 1000,
                "from": {
                    "id": test_user,
                    "is_bot": False,
                    "first_name": "Test",
                    "last_name": "User",
                    "language_code": "zh-hans"
                    },
                "chat": {
                    "id": test_user,
                    "first_name": "Test",
                    "last_name": "User",
                    "type": "private"
                    },
                "date": 1000000000,
                "text": "foo"
                }
            }
        environ = create_environ(
            method='POST',
            data=dumps(update)
        )
        request = Request(environ)
        result = webhook(request)
        print(result)
        self.assertEqual(result, 'ok')
