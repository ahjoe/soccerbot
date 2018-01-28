""" Test string methods builtin in python 3

This test demostrates how to run unit test in vscode

Example:
    $ python stringtest.py

Attributes:

"""
import os
import unittest
import logging

#
# TODO: todo example here
# FIXME: fixme example here
#

# ====================
# logger configuration
# ====================
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '[%(asctime)s.%(msecs)03d] %(name)s %(levelname)-8s: %(message)s'
    , '%Y-%m-%d %H:%M:%S'
    )

# create console handler and append into logger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# create file handler and append into logger
LOG_RELATIVE_PATH = '/../log/soccerbot.log'
fh = logging.FileHandler(
    os.path.dirname(os.path.realpath(__file__))
    + LOG_RELATIVE_PATH)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
# =======================

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        logger.info('start running test_isupper')
        self.assertTrue('FOO'.isupper())
        self.assertFalse('foo'.isupper())
        logger.info('end running test_isupper')

    @unittest.skip("This test would be skipped")
    def test_skip(self):
        # do nothing
        i = 1
        self.assertTrue(i == 1)

if __name__ == '__main__':
    unittest.main()
