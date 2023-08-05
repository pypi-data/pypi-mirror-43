from copy import deepcopy

from django.template.library import Library
from django.template.base import Node, FilterExpression
from django.template.defaulttags import URLNode, url, TemplateSyntaxError
from django.urls import reverse

register = Library()


class LocaleNode(Node):
    def __init__(self, nodelist, kwargs):
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context):
        value = context[self.kwargs['key']]
        if value:
            context[self.kwargs['as_key']] = value.get_locale(context['language'])
            nodelist = self.nodelist.render(context)
            del context[self.kwargs['as_key']]
            return nodelist
        return ''


class TranslationNode(Node):
    def __init__(self, args):
        self.args = args

    def render(self, context):
        if self.args and len(self.args) == 1:
            resolver_match = deepcopy(context['request'].resolver_match)
            if context[self.args[0]].is_default:
                resolver_match.kwargs.pop('language', None)
            else:
                resolver_match.kwargs['language'] = context[self.args[0]].code
            return reverse(resolver_match.url_name, args=resolver_match.args, kwargs=resolver_match.kwargs)

        raise TemplateSyntaxError("""
            For working need:
                1. language instance.
        """)


class LocaleURLNode(URLNode):
    def __init__(self, parser, url_node):
        self.parser = parser
        super().__init__(url_node.view_name, url_node.args, url_node.kwargs, url_node.asvar)

    def render(self, context):
        if not context['language'].is_default:
            language = self.parser.compile_filter('language.code')

            if self.args:
                if self.args[0].resolve(context) != language.resolve(context):
                    self.args.insert(0, language)

            elif self.kwargs:
                self.kwargs['language'] = language

            else:
                self.args.insert(0, language)

        return super().render(context)


@register.tag(name='bl_locale')
def base_locale_with_tag(parser, token):
    nodelist = parser.parse(('end_bl_locale',))
    parser.delete_first_token()
    args = token.split_contents()
    if len(args) == 4 and args[2] == 'as':
        kwargs = {'key': args[1], 'as_key': args[-1]}
        return LocaleNode(nodelist, kwargs)
    raise TemplateSyntaxError("""
    For working locale tag need:
        1. Instance, with type BaseModel.
        2. Name, for use in tag.
    """)


@register.tag(name='bl_trans_url')
def base_locale_translation_url(parser, token):
    args = token.split_contents()
    return TranslationNode(args[1:])


@register.tag(name='bl_url')
def base_locale_url(parser, token):
    url_node = url(parser, token)
    return LocaleURLNode(parser, url_node)


@register.filter(name='bl_locale')
def base_locale_filter(base_model, language):
    if base_model.locales:
        return base_model.locales.filter(language=language).first()
    return None
