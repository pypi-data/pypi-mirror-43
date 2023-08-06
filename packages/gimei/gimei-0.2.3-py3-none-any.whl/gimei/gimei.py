# -*- coding: utf-8 -*-
import random
import yaml
from functools import wraps

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .address import Address
from .name import Name


MALE = 'male'
FEMALE = 'female'
GENDER = (MALE, FEMALE)


def cache(f):
    saved = {}

    @wraps(f)
    def wrapper(file_path):
        if file_path in saved:
            return saved[file_path]
        result = f(file_path, mode='r')
        saved[file_path] = result
        return result
    return wrapper


@cache
def yaml_load(file_path, mode='r'):
    import os
    file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    try:
        f = open(file_dir + '/' + file_path, mode, encoding='utf-8')
    except IOError:
        raise Exception("Can not open {}".format(file_dir + '/' + file_path))
    return yaml.load(f, Loader=Loader)


class Gimei(object):
    NAMES = yaml_load('./data/names.yml')
    ADDRESSES = yaml_load('./data/addresses.yml')

    def __init__(self, gender=None):
        if gender is None:
            gender = random.choice(GENDER)
        self.gender = gender

    @property
    def name(self):
        return Name(self.gender)

    @property
    def address(self):
        return Address()
