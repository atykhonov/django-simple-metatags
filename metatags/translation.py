from modeltranslation.translator import translator, TranslationOptions

from .models import MetaTag


class MetaTagTranslationOptions(TranslationOptions):
    fields = ('title', 'h1', 'description')

translator.register(MetaTag, MetaTagTranslationOptions)
