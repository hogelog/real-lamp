'''
Created on 2012/03/25

@author: hogelog
'''
import unittest
from controler import HttpControler, BaseHttpControlerHandler
import requests


class Test(unittest.TestCase):
    def setUp(self):
        self.controler = HttpControler("0.0.0.0", 12345,
                                       BaseHttpControlerHandler)
        self.controler.start()

    def tearDown(self):
        self.controler.shutdown()

    def testIndex(self):
        res = requests.get("http://127.0.0.1:12345/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.read(), "Hello Http Controler!")

if __name__ == "__main__":
    unittest.main()
