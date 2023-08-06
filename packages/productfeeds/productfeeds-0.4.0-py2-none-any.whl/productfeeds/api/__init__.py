
class AbstractImporterAPIException(Exception):
    pass


class AbstractImporterAPI(object):
    def __init__(self, prefix='', *args, **kwargs):
        self.prefix = prefix
        self.storage = kwargs['storage']
        self.prefix = prefix
        self.tmp_dir = kwargs['tmp_dir']

    def _get_articlecode(self, product_id):
        prefix = ''
        if self.prefix:
            prefix = self.prefix

        return "{}{}".format(prefix, product_id)

    def import_products(self):
        raise AbstractImporterAPIException("Implement me! :)")
