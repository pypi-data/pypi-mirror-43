import glob
import importlib
import ntpath
from os.path import dirname

__IMPORTER_MODULES_TO_LOAD = [
    ntpath.basename(file_path).replace(".py", "") for file_path in glob.glob(dirname(__file__)+"/api/*api.py")
]


def load_importer_apis():
    importers = {}
    for my_module in __IMPORTER_MODULES_TO_LOAD:
        my_class = my_module.upper()[0] + my_module[1:-3] + my_module.upper()[-3:]
        my_module_object = importlib.import_module("productfeeds.api.{}".format(my_module))
        importers[my_module[:-3]] = getattr(my_module_object, my_class)
    return importers
