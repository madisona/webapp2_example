
import unittest

from google.appengine.ext import testbed, db

__all__ = (
    'BaseAppEngineTestCase',
)

class BaseAppEngineTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()