'''Unit testing'''

from unittest import TestCase
from nose.tools import *

class ExampleTest(TestCase):
    '''A cute little test.'''
    def test_add(self):
        assert_equal(1 + 1, 2)
