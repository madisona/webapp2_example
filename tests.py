
import unittest

import main

class MyTest(unittest.TestCase):

    def test_returns_200(self):
        response = main.app.get_response('/')
        self.assertEqual(200, response.status_int)

if __name__ == '__main__':
    unittest.main()