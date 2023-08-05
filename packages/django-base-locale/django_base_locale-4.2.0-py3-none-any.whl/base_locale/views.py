from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.utils import translation
from django.urls import reverse

from base_locale.models import Language


class BaseLocaleMixin(ContextMixin):
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('language') and context['language'].is_default:
            request.resolver_match.kwargs.pop('language', None)
            return redirect(reverse(request.resolver_match.url_name, args=request.resolver_match.args,
                                    kwargs=request.resolver_match.kwargs))
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_language = int(bool(kwargs.get('language')))
        context['languages'] = Language.objects.all()
        context['language'] = context['languages'].filter(
            **{('is_default', 'code')[is_language]: (True, kwargs.get('language'))[is_language]}).first()

        translation.activate(context['language'].code)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = context['language'].code
        return context
