import re

from importlib import import_module

from django.conf import settings


def get_language_cls():
    return getattr(settings, 'BASE_LOCALE_LANGUAGE_CLASS', getattr(import_module('base_locale.models'), 'Language'))


def generate_fk_name_from_cls_name(cls_name):
    return '_'.join(re.findall(r'[A-Z]+[a-z]+', cls_name)).lower()


def check_base_model_locale(cls_name):
    if cls_name.endswith('Locale'):
        return True
    return False


def generate_base_model_cls_name(cls_name):
    if cls_name.endswith('Locale'):
        return ''.join(re.findall(r'[A-Z]+[a-z]+', cls_name)[:-1])
    raise NameError('{} class must end with \'Locale\''.format(cls_name))
