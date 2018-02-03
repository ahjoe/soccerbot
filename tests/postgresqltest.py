""" Test data read/write data from postgreSQL database

This test demostrates how to persist data into postgreSQL database

Example:
    $ python postgresqltest.py

Attributes:

"""
import os
import unittest
import logging
import urllib.request
import json
import psycopg2
import psycopg2.extras

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


# =======================
# psycopg2 configuration
# =======================

# =======================


class TestReadWritePostgreSQL(unittest.TestCase):
    def test_connect(self):
        try:
            conn = psycopg2.connect(
                host="35.229.71.219"
                , database="soccerbot"
                , user="botsqlreader"
                , password="yattong"
            )
            logger.info(conn.dsn)
            self.assertFalse(conn.closed)
        except psycopg2.Error as ex:
            logger.error(
                'Failed to connect. Invalid host, database, user or password. Aborting. ' +
                'Exception: %s'
                , ex
            )
            self.assertRaises(psycopg2.Error)

    def test_read(self):
        try:
            # make connection
            conn = psycopg2.connect(
                host="35.229.71.219"
                , database="soccerbot"
                , user="botsqlreader"
                , password="yattong"
            )
            logger.info(conn.dsn)
            # get cursor with dict support
            cr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # read table
            # WHERE source = 'api.football-data.org'
            # AND version = 'v1'
            # AND category ='fixtures'
            # ORDER BY category_id
            cr.execute("""
                        SELECT * 
                        FROM jsons 
                       """)
            rows = cr.fetchall()
            for row in rows:
                p = 'http'
                s = row['source']
                v = row['version']
                c = row['category']
                cid = '' if row['category_id'] < 0 else row['category_id']
                sc = row['sub_category']
                scid = '' if row['sub_category_id'] < 0 else row['sub_category_id']
                o = row['options']
                source = 'source: {0}://{1}/{2}/{3}/{4}/{5}/{6}/?{7}'.format(*[p, s, v, c, cid, sc, scid, o])
                logger.info(source)
                jsonData = row['data']
                logger.info(
                    json.dumps(jsonData, indent=4, sort_keys=True)
                )
        except psycopg2.Error as ex:
            logger.error(
                'Failed to connect database or read table. Aborting. ' +
                'Exception: %s'
                , ex
            )
            self.assertRaises(psycopg2.Error)

    def test_write(self):
        try:
            # define variables
            '''
            protocol = 'http'
            source = 'api.football-data.org'
            version = 'v1'
            category = 'fixtures'
            categoryId = 159084
            subCategory = ''
            subCategoryId = -1
            options = 'head2head=0'
            '''
            '''
            protocol = 'http'
            source = 'api.football-data.org'
            version = 'v1'
            category = 'teams'
            categoryId = 5
            subCategory = ''
            subCategoryId = -1
            options = ''
            '''
            '''
            protocol = 'http'
            source = 'api.football-data.org'
            version = 'v1'
            category = 'teams'
            categoryId = 5
            subCategory = 'players'
            subCategoryId = -1
            options = ''
            '''
            protocol = 'http'
            source = 'api.football-data.org'
            version = 'v1'
            category = 'competitions'
            categoryId = -1
            subCategory = ''
            subCategoryId = -1
            options = ''
            # get json from url
            # e.g http://api.football-data.org/v1/fixtures/159084?head2head=0
            # e.g http://api.football-data.org/v1/teams/5
            # e.g http://api.football-data.org/v1/teams/5/players
            # e.g http://api.football-data.org/v1/competitions
            kwargs = {'p': protocol,
                      's': source,
                      'v': version,
                      'c': category,
                      'cid': '' if categoryId < 0 else categoryId,
                      'sc': subCategory,
                      'scid':  '' if subCategoryId < 0 else subCategoryId,
                      'o': options}
            url = '{p}://{s}/{v}/{c}/{cid}/{sc}/{scid}/?{o}'.format(**kwargs)
            print(url)
            req = urllib.request.Request(url=url, headers={}, method=None)
            res = urllib.request.urlopen(req, timeout=5)
            data = res.read()
            encoding = res.info().get_content_charset('utf-8')
            JSONdata = json.loads(data.decode(encoding))
            logger.info(
                json.dumps(JSONdata, indent=4, sort_keys=True)
            )
            # make connection
            conn = psycopg2.connect(
                host="35.229.71.219"
                , database="soccerbot"
                , user="botsqlwriter"
                , password="yattong4ever"
            )
            logger.info(conn.dsn)
            # get cursor
            cr = conn.cursor()
            cr.execute(
                """INSERT INTO jsons(source, version, category, category_id, sub_category, sub_category_id, options, data)
                   VALUES (%(s)s, %(v)s, %(c)s, %(cid)s, %(sc)s, %(scid)s, %(o)s, %(data)s);"""
                , {'s':source,
                   'v':version,
                   'c':category,
                   'cid':categoryId,
                   'sc':subCategory,
                   'scid':subCategoryId,
                   'o':options,
                   'data':json.dumps(JSONdata)}
            )
            # commit transaction
            conn.commit()
            # close
            cr.close()
            conn.close()
        except psycopg2.Error as ex:
            logger.error(
                'Failed to connect database or url-get json or write table. Aborting. ' +
                'Exception: %s'
                , ex
            )
            self.assertRaises(psycopg2.Error)

if __name__ == '__main__':
    unittest.main()
