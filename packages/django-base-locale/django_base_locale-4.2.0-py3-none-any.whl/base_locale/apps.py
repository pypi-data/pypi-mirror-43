from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BaseLocaleConfig(AppConfig):
    name = 'base_locale'
    verbose_name = _('Localization')
