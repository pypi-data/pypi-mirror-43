import sys

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models.base import ModelBase

from base_locale.utils import (
    get_language_cls, generate_fk_name_from_cls_name, generate_base_model_cls_name,
)

from base_locale.exceptions import (
    BaseModelNotFound, BaseModelLocaleNotFound, BaseModelForeignKeyNotFound,
)


class ModelBaseLocale(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        if not new_class._meta.abstract:
            base_cls_name = generate_base_model_cls_name(new_class.__name__)
            base_cls = getattr(sys.modules[new_class.__module__], base_cls_name, None)
            if not base_cls:
                raise BaseModelNotFound('Not found class: \'{}\' in module: \'{}\''.format(
                    base_cls_name, new_class.__module__))
            new_class.add_to_class(generate_fk_name_from_cls_name(base_cls_name),
                                   models.ForeignKey(base_cls, on_delete=models.CASCADE))
        return new_class


class Language(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name=_('Code'))
    title = models.CharField(max_length=64, unique=True, verbose_name=_('Title'))
    is_default = models.BooleanField(default=False, verbose_name=_('Default'))
    image = models.FileField(upload_to='language/', verbose_name=_('Image'), blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.code.upper()

    @property
    def slug(self):
        return '' if self.is_default else '/{}'.format(self.code)

    def image_admin(self):
        if self.image:
            return mark_safe('<img height="50px" src="{}">'.format(self.image.url))
        return ''

    image_admin.short_description = _('Image')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_default:
            type(self).objects.update(is_default=False)
        self.code = self.code.lower()
        super(Language, self).save(force_insert, force_update, using,
                                   update_fields)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class BaseModel(models.Model):
    @property
    def locales(self):
        if not self._locale_class:
            raise BaseModelLocaleNotFound('Not found class: \'{}\' in module: \'{}\''.format(
                type(self).__name__, self.__module__))
        return self._locale_class.objects.filter(**{self._locale_fk_name: self})

    @property
    def locale_default(self):
        return self.locales.filter(language__is_default=True).first() or self.locales.order_by('language').first()

    def get_locale(self, language):
        return self.locales.filter(language=language).first()

    @property
    def _locale_fk_name(self):
        return generate_fk_name_from_cls_name(type(self).__name__)

    @property
    def _locale_class(self):
        return getattr(sys.modules[self.__module__], '{}Locale'.format(type(self).__name__), None)

    def __str__(self):
        return self.locale_default.language.code.upper()

    class Meta:
        abstract = True


class BaseModelLocale(models.Model, metaclass=ModelBaseLocale):
    language = models.ForeignKey(get_language_cls(), on_delete=models.CASCADE, verbose_name=_('Language'))

    def __str__(self):
        return self.language.code.upper()

    @property
    def _base_model_name(self):
        return generate_base_model_cls_name(type(self).__name__)

    @property
    def base(self):
        base_model_instance = getattr(self, generate_fk_name_from_cls_name(self._base_model_name), None)
        if not base_model_instance:
            raise BaseModelForeignKeyNotFound('Not fount attribute: \'\' in class: \'\' in module: \'\''.format(
                generate_fk_name_from_cls_name(self._base_model_name), type(self).__name__, self.__module__))
        return base_model_instance

    class Meta:
        abstract = True
