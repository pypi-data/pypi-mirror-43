import logging

from productfeeds.utils import load_importer_apis
from .storage.mysqlstorage import MySQLStorage

IMPORTERS = load_importer_apis()

logger = logging.getLogger(__name__)


def get_importer_instance(importer, config, storage=None):
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
    return IMPORTERS[importer](storage=storage, **config)


def import_feeds_to_mysql_table(importers_config, mysql_config):
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
    for importer in importers_config:
        storage = MySQLStorage(mysql_config)
        storage.clear()
        api = get_importer_instance(importer['api'], importer['config'], storage=storage)
        result = api.import_products()
        logger.info("Import status: %s", result)
