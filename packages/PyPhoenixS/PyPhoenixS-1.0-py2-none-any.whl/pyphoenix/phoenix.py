import phoenixdb
import phoenixdb.cursor
from pyphoenix.exc import *

paramstyle = 'pyformat'

def connect(*args, **kwargs):
    """Constructor for creating a connection to the database. See class :py:class:`Connection` for
    arguments.
    :returns: a :py:class:`Connection` object.
    """
    return Connection(*args, **kwargs)

class Connection(object):

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        database_url = 'http://%(host)s:%(port)s/' % kwargs
        self._conn = phoenixdb.connect(database_url, autocommit=True)

    def close(self):
        # TODO cancel outstanding queries?
        pass

    def commit(self):
        """Phoenix does not support transactions"""
        pass

    def cursor(self):
        """Return a new :py:class:`Cursor` object using the connection."""
        return self._conn.cursor()

    def rollback(self):
        pass
