""" Test for url request & response handlers via python v3 builtin modules

This test demostrates how to read json response through url path

Example:
    $ python urltest.py

Attributes:

"""

import os
import unittest
import logging
import urllib.request
import json

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

class TestUrlJson(unittest.TestCase):
    def test_readjson(self):
        url = 'http://api.football-data.org/v1/teams/5'
        # =============
        # proxy support
        # ref: https://docs.python.org/3.5/howto/urllib2.html#proxies
        #==============
        ph = urllib.request.ProxyHandler(
            proxies={'http': 'http://proxy.ha.org.hk:8080'}
            )
        opener = urllib.request.build_opener(ph)
        urllib.request.install_opener(opener)
        # =============
        req = urllib.request.Request(url=url, headers={}, method=None)
        res = urllib.request.urlopen(req, timeout=5)
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')
        JSONdata = json.loads(data.decode(encoding))
        logger.info(
            json.dumps(JSONdata, indent=4, sort_keys=True)
        )
        self.assertTrue(JSONdata != None)


if __name__ == '__main__':
    unittest.main()
