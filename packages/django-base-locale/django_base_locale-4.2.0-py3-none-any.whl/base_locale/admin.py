from django.contrib import admin

from base_locale.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('image_admin', 'title', 'code', 'is_default',)
    list_display_links = ('image_admin', 'title', 'code', 'is_default',)
