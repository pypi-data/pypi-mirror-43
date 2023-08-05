from django.urls import re_path, path, include


def include_base_locale_urls(urls):
    return include([re_path(r'^(?P<language>[a-z]{2})/', include(urls)), path('', include(urls))])
