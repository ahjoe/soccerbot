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

if __name__ == '__main__':
    unittest.main()
