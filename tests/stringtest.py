""" Test string methods builtin in python 3

This test demostrates how to run unit test in vscode

Example:
    $ python stringtest.py

Attributes:

"""
import unittest

#
# TODO:
# FIXME:
#
class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('foo'.isupper())

    @unittest.skip("This test would be skipped")
    def test_skip(self):
        # do nothing
        i = 1
        self.assertTrue(i == 1)

if __name__ == '__main__':
    unittest.main()
