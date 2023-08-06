
class AbstractStorageException(Exception):
    pass


class AbstractStorage(object):

    def save_product(self, product):
        raise AbstractStorage('Implement me! :)')
