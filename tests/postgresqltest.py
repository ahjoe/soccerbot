""" Test data read/write data from postgreSQL database

This test demostrates how to persist data into postgreSQL database

Example:
    $ python postgresqltest.py

Attributes:

"""
import os
import unittest
import logging
import psycopg2

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
        except ConnectionAbortedError as ex:
            logger.Error(
                'Failed to connect. Invalid host, database, user or password. Aborting'
                , ex
            )

    def test_read(self):
        self.assertTrue(1 == 1)

    def test_write(self):
        self.assertTrue(1 == 1)

if __name__ == '__main__':
    unittest.main()
