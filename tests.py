
import os
from unittest import TestCase

import utils

class IsDevelTests(TestCase):

    def setUp(self):
        self.old_val = os.environ.get('SERVER_SOFTWARE')

    def tearDown(self):
        if self.old_val:
            os.environ['SERVER_SOFTWARE'] = self.old_val
        else:
            del(os.environ['SERVER_SOFTWARE'])

    def test_server_software_is_dev(self):
        os.environ['SERVER_SOFTWARE'] = 'Development Version 1.5'
        self.assertEqual(True, utils.is_devel())

    def test_server_software_is_not_dev(self):
        os.environ['SERVER_SOFTWARE'] = 'Production Version 1.5'
        self.assertEqual(False, utils.is_devel())

class SlugifyTests(TestCase):

    def test_slugify_replaces_non_alphanumeric_characters_with_hyphen(self):
        string = u'My Cool. Event Starts! Tomorrow'
        self.assertEqual('my-cool-event-starts-tomorrow', utils.slugify(string))

    def test_strips_trailing_special_characters(self):
        string = u'ending_something!!!'
        self.assertEqual('ending-something', utils.slugify(string))

    def test_strips_leading_special_characters(self):
        string = u'++starting_something'
        self.assertEqual('starting-something', utils.slugify(string))

    def test_sends_characters_to_lower_case(self):
        string = u'ABC'
        self.assertEqual('abc', utils.slugify(string))

class IntGetTests(TestCase):

    def test_returns_int_val_when_possible(self):
        self.assertEqual(10, utils.intget("10"))

    def test_returns_none_when_val_is_not_integer(self):
        self.assertEqual(None, utils.intget("10.32"))

    def test_returns_default_when_val_is_not_integer_and_default_given(self):
        self.assertEqual(0, utils.intget("ABC", 0))