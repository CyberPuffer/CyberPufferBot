# -*- coding: utf-8 -*-
from functions import luck
from datetime import datetime
import unittest

class Test_Functions_Luck(unittest.TestCase):
    def test_get_luck(self):
        test_time = datetime(2000, 1, 1, 0, 0)
        test_uid = 100000000
        self.assertEqual(luck.get_luck(test_uid,test_time), u'当前人品：★★★★☆')

if __name__ == '__main__':
    unittest.main()