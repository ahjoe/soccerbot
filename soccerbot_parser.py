""" soccerbot Parser Classes

Base Parser Class for Soccerbot

Example:
    $ python soccerbot_parser.py

Attributes:

"""

from soccerbot import Soccerbot
from soccerbot import logger as botLogger
import urllib.request
import json

# =============
# Base Parser
# =============

class SoccerbotParser:
    def __init__(self, bot):
        self.bot = bot
        self.url = ''

    def parse(self):
        botLogger.debug('Base Parser: %s', self)
        botLogger.debug('Parser bot: %s', self.bot)

    def getJSONdata(self, urlconf):
        self.url = '{p}://{s}/{v}/{c}/{cid}/{sc}/{scid}/?{o}'.format(**urlconf)
        botLogger.debug('url to be parsed: %s', self.url)
        req = urllib.request.Request(url=self.url, headers={}, method=None)
        res = urllib.request.urlopen(req, timeout=5)
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')
        JSONdata = json.loads(data.decode(encoding))
        botLogger.debug('url successfully parsed: %s', self.url)
        botLogger.debug(
            json.dumps(JSONdata, indent=4, sort_keys=True)
        )
        return JSONdata

    def persist(self, dbvalues):
        self.bot.dbcur.execute(
            """INSERT INTO jsons(source, version, category, category_id, sub_category, sub_category_id, options, data)
                VALUES (%(s)s, %(v)s, %(c)s, %(cid)s, %(sc)s, %(scid)s, %(o)s, %(data)s);"""
            , dbvalues
        )
        # commit transaction
        self.bot.dbconn.commit()
        botLogger.debug('JSON on url [%s] successfully persisted.', self.url)

    def __del__(self):
        botLogger.debug('performing destruction of %s...', self.__class__.__name__)
        botLogger.debug('successful destruction of %s.', self.__class__.__name__)

    # static factory method for choosing proper parser
    @staticmethod
    def getParser(bot):
        if bot:
            if bot.api == 'api.football-api.org':
                return SoccerbotParserFootballApiOrg(bot)
        return SoccerbotParser(bot)

# ================
# Concrete Parsers
# ================

class SoccerbotParserFootballApiOrg(SoccerbotParser):
    def parse(self):
        botLogger.debug('Concrete Parser: %s', self)
        botLogger.debug('Parser bot: %s', self.bot)
        botLogger.debug('Parser botapi = %s', self.bot.api)
        botLogger.debug('Parser botdbconf = %s', self.bot.dbconf)
        botLogger.debug('Parser botdbconn dsn = %s', self.bot.dbconn.dsn)
        botLogger.debug('Parser botdbcur = %s', self.bot.dbcur)
        #
        # implementation on RESTful API : api.football-api.org
        # only consider England Premier League 2017/18
        # http://api.football-data.org/v1/competitions/445
        #
        protocol = 'http'
        source = 'api.football-data.org'
        version = 'v1'
        category = 'competitions'
        categoryId = '445'
        subCategory = ''
        subCategoryId = ''
        options = ''
        urlconf = {'p': protocol,
                   's': source,
                   'v': version,
                   'c': category,
                   'cid': categoryId,
                   'sc': subCategory,
                   'scid': subCategoryId,
                   'o': options
                  }
        # get json data
        JSONdata = self.getJSONdata(urlconf)
        if JSONdata:
            # =======================
            # construct dbvalues dict
            # =======================
            dbvalues = {'s': source,
                        'v': version,
                        'c': category,
                        'cid': -1 if not categoryId else int(categoryId),
                        'sc': subCategory,
                        'scid': -1 if not subCategoryId else int(subCategoryId),
                        'o': options,
                        'data': json.dumps(JSONdata)
                       }
            self.persist(dbvalues)
            # TODO: further grep data from links stored in JSONdata
            # http://api.football-data.org/v1/competitions/445/teams
            # http://api.football-data.org/v1/competitions/445/fixtures
            # http://api.football-data.org/v1/competitions/445/leagueTable


# test
if __name__ == "__main__":
    # instancing soccerbot
    api1 = 'api.football-api.org'
    db1conf = {'host':'35.229.71.219',
               'database':'soccerbot',
               'user':'botsqlwriter',
               'password':'yattong4ever'
              }
    bot1 = Soccerbot(api=api1, dbconf=db1conf)
    # instancing soccerbot parser
    botParser1 = SoccerbotParser.getParser(bot=bot1)
    botLogger.info('perform self class test %s(api=%s)', botParser1.__class__.__name__, botParser1.bot.api if botParser1.bot else None)
    botLogger.info('botParser-bot = %s', botParser1.bot)
    # parse api calls
    botParser1.parse()
    del botParser1
    del bot1
