import os.path as path

from forge import ForgeConfig
import logging

logger=logging.getLogger('ec-config')

app_config = path.join(path.dirname(__file__), "forge.toml")

forge_config = ForgeConfig(app_config)

db_path = path.join(forge_config.get_app_path(), "ec.db")
logger.info('db_path: {}'.format(db_path))
