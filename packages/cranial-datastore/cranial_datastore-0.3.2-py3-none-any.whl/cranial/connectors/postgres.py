import logging
import io
import os

from cranial.connectors import base
from cranial.common import logger

log = logger.get('CONNECTOR_POSTGRES_LOGLEVEL', name='postgres_connector')


class InMemoryConnector(base.Connector):
    def __init__(self, conn, db='', binary=True, do_read=False):
        super().__init__(base_address=db, binary=binary, do_read=do_read)

    def get(self, query):
        """
        Get a bytes stream of a query result.
        """
        def generator():
	    # This use of a "named" cursor is the psycopg extension that makes
	    # this not quite DBAPI2 compliant.
            cursor = self.conn.cursor(query)
            cursor.execute(query)
            for row in cursor:
                # @TODO? This may not be the best way to convert to bytes...
                yield str(row)

        return base.iterable_to_strem(generator())


    def put(self, source, table, serializer):
        raise Exception('Not implemented.')
