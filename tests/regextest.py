""" Test regex functions

This test demostrates how to manuiplate regex functions

Example:
    $ python regextest.py

Attributes:

"""
import os
import unittest
import logging
import re
from urllib.parse import urlparse

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
LOG_RELATIVE_PATH = '/../log/soccerbot_test.log'
fh = logging.FileHandler(
    os.path.dirname(os.path.realpath(__file__))
    + LOG_RELATIVE_PATH)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
# =======================

class TestRegex(unittest.TestCase):
    def test_regex(self):
        url = 'https://api.football-data.org/v1/competitions/445/'
        #pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        pattern = r'(?P<protocol>http[s]?)+'
        #pattern = r'(?P<protocol>http[s]?)://(?P<source>[a-zA-Z]|[0-9]|[$-_@.&+]+)/+'
        m = re.match(pattern, url)
        if m.group:
            logger.info('protocol= %s', m.group('protocol'))
            #logger.info('source= %s', m.group('source'))

    def test_urlparse(self):
        url = 'http://api.football-data.org/v1/fixtures/159084?head2head=0'
        res = urlparse(url)
        logger.info('urlparse = [%s]', res)
        logger.info('scheme = [%s]', res[0])
        logger.info('netloc = [%s]', res[1])
        logger.info('path = [%s]', res[2])
        logger.info('params = [%s]', res[3])
        logger.info('query = [%s]', res[4])
        logger.info('fragment = [%s]', res[5])

if __name__ == '__main__':
    unittest.main()
