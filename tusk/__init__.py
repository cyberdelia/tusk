# -*- coding: utf-8  -*-
import binascii
import os
import psycopg2

from contextlib import contextmanager

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse  # noqa


class TuskException(Exception):
    pass


class Lock(object):
    def __init__(self, name, dsn=None):
        dsn = dsn or os.environ.get('DATABASE_URL')
        if dsn is None:
            raise ValueError("You must specify a DSN.")
        params = urlparse(dsn)
        self.conn = psycopg2.connect(database=params.path[1:], user=params.username,
                                     password=params.password, host=params.hostname,
                                     port=params.port)
        self.conn.autocommit = True
        self.key = self._key(name)

    @contextmanager
    def cursor(self):
        try:
            cursor = self.conn.cursor()
            yield cursor
        except psycopg2.Error as e:
            raise TuskException(e)
        finally:
            cursor.close()

    def _key(self, name):
        i = binascii.crc32(name.encode('utf-8'))
        if i > 2147483647:
            return -(-(i) & 0xffffffff)
        return i

    def acquire(self, blocking=True, space=-2147483648):
        with self.cursor() as cursor:
            if blocking:
                cursor.execute("SELECT pg_advisory_lock(%s, %s);", (space, self.key))
                return True
            else:
                cursor.execute("SELECT pg_try_advisory_lock(%s, %s);", (space, self.key))
                return cursor.fetchone()[0]

    __enter__ = acquire

    def release(self, space=-2147483648):
        with self.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_unlock(%s, %s);", (space, self.key))
            return cursor.fetchone()[0]

    def __exit__(self, type, value, traceback):
        self.release()
