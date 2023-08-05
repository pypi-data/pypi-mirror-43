"""This module contains function that can help you in different situations"""
import importlib
import inspect
import os


def import_cards(path, base_module_name, parent_class):
    """
    Allows you to dinamically import cards based on their type,
    check munchkinapi.models.cards.treasures for an example of usage
    """
    path = path.replace('__init__.pyc', '').replace('__init__.py', '')
    cards = []
    files = os.listdir(path)
    files.remove('__init__.py')
    for file in files:
        if file.endswith('.py'):
            module_name = file.replace('.py', '')
            module_name = '%s.%s' % (base_module_name, module_name)
            module = importlib.import_module(module_name)
            for obj_name in dir(module):
                obj = getattr(module, obj_name)
                if obj != parent_class and inspect.isclass(obj) and issubclass(obj, parent_class):
                    cards.append(obj)

    return cards
