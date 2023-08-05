import logging

from event_chain.config import config
from event_chain.db import utils

logger = logging.getLogger('ec-db-init')

if __name__ == '__main__':
    db = config.db_path
    logger.info('Connecting to db {}'.format(db))
    conn = utils.create_connection()
    utils.init_db(conn)
    conn.close()
