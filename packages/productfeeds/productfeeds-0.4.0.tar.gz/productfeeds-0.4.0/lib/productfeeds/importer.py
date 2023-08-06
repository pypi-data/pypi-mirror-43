import logging

from productfeeds.utils import load_importer_apis
from .storage.mysqlstorage import MySQLStorage

IMPORTERS = load_importer_apis()

logger = logging.getLogger(__name__)


def get_importer_instance(importer, config, storage=None, tmp_dir=""):
    """
    Instantiate importer object by given settings
    Args:
        importer (str): Importer name
        config (dict): Importer settings
        storage (storage.AbstractStorage): Storage object
    Return:
        api (ImporterAbstractAPI): The importer API object
    Raises:
        None
    """
    return IMPORTERS[importer](storage=storage, tmp_dir=tmp_dir, **config)


def import_feeds_to_mysql_table(importers_config, mysql_config, tmp_dir=''):
    """
    Imports feed using passed importer to MySQL table
    Args:
        importers_config (dict): Importer configuration
        mysql_config (dict): MySQL configuration

    Return:
        None
    Raises:
        None
    """
    storage = MySQLStorage(mysql_config)
    storage.clear()
    for importer in importers_config:
        api = get_importer_instance(importer['api'], importer['config'], storage=storage, tmp_dir=tmp_dir)
        result = api.import_products()
        logger.info("Import status: %s", result)
