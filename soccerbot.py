""" soccerbot Main Class

The bot calls some RESTful API providers and persists json data into postgreSQL database

Example:
    $ python soccerbot.py

Attributes:

"""
import os
import logging
#import urllib.request
#import json
import psycopg2
import psycopg2.extras

# ====================
# logger configuration
# ====================
# create logger
logger = logging.getLogger()
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
LOG_RELATIVE_PATH = '/log/soccerbot.log'
fh = logging.FileHandler(
    os.path.dirname(os.path.realpath(__file__))
    + LOG_RELATIVE_PATH)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
# =======================

class Soccerbot:
    def __init__(self, api, dbconf):
        logger.name = self.__class__.__name__
        self.api = api
        self.dbconf = dbconf
        self.dbconn = self.connect()
        if self.dbconn:
            # get cursor with dict support
            self.dbcur = self.dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if self.dbcur:
                # get parser
                pass

    def __del__(self):
        try:
            logger.debug('performing destruction of %s...', self.__class__.__name__)
            if self.dbconn:
                if self.dbcur:
                    self.dbcur.close()
                self.dbconn.close()
            logger.debug('successful destruction of %s.', self.__class__.__name__)
        except psycopg2.Error as ex:
            logger.error(
                'Failed to close cursor and connection. Quitting. ' +
                'Exception: %s'
                , ex
            )

    def connect(self):
        try:
            logger.debug(self.dbconf)
            conn = psycopg2.connect(**self.dbconf)
            logger.debug(conn.dsn)
            return conn
        except psycopg2.Error as ex:
            logger.error(
                'Failed to connect. Invalid host, database, user or password. Aborting. ' +
                'Exception: %s'
                , ex
            )
            return None

# test
if __name__ == "__main__":
    # instancing soccerbot
    api1 = 'api.football-api.org'
    db1conf = {'host':'35.229.71.219',
               'database':'soccerbot',
               'user':'botsqlreader',
               'password':'yattong'
              }
    bot = Soccerbot(api=api1, dbconf=db1conf)
    logger.info('perform self class test %s(api=%s)', bot.__class__.__name__, api1)
    logger.info('api = %s', bot.api)
    logger.info('dbconf = %s', bot.dbconf)
    logger.info('dbconn dsn = %s', bot.dbconn.dsn)
    logger.info('dbcur = %s', bot.dbcur)
    del bot
