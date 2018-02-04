""" Test JSON functions

This test demostrates how to manuiplate json functions

Example:
    $ python postgresqltest.py

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

class TestJSON(unittest.TestCase):
    def test_json_get_attr_1(self):
        url = 'http://api.football-data.org/v1/competitions/445/'
        req = urllib.request.Request(url=url, headers={}, method=None)
        res = urllib.request.urlopen(req, timeout=5)
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')
        JSONdata = json.loads(data.decode(encoding))
        logger.info(
            json.dumps(JSONdata, indent=4, sort_keys=True)
        )
        fixturesUrl = JSONdata['_links']['fixtures']['href']
        logger.info(fixturesUrl)
        teamsUrl = JSONdata['_links']['teams']['href']
        logger.info(teamsUrl)
        leagueTableUrl = JSONdata['_links']['leagueTable']['href']
        logger.info(leagueTableUrl)
        self.assertTrue(fixturesUrl)
        self.assertTrue(teamsUrl)
        self.assertTrue(leagueTableUrl)

if __name__ == '__main__':
    unittest.main()
