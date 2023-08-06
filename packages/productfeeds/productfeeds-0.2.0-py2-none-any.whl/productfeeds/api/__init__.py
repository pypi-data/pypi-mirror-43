
class AbstractImporterAPIException(Exception):
    pass


class AbstractImporterAPI(object):

    def import_products(self):
        raise AbstractImporterAPIException("Implement me! :)")
