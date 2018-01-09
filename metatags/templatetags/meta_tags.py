from django.template import Library
from django.utils.encoding import force_text

from metatags.models import MetaTag


register = Library()


def _get_model_instance_title(model_instance, model_title_field):
    return getattr(model_instance, model_title_field, force_text(model_instance))


@register.inclusion_tag('metatags/_meta_tags.html', takes_context=True)
def include_meta_tags(context, model_instance=None, model_title_field='title',
                      default_title='', default_h1='', default_description=''):
    if model_instance is not None:
        # Getting meta tags for a given model instance.
        try:
            meta_tags = MetaTag.objects.get(object_id=model_instance.pk,
                                            content_type__app_label=model_instance._meta.app_label,
                                            content_type__model=model_instance._meta.model_name)
            meta_tags.title = meta_tags.title or _get_model_instance_title(model_instance, model_title_field)
            meta_tags.h1 = meta_tags.h1 or default_h1
            meta_tags.description = meta_tags.description or default_description
        except MetaTag.DoesNotExist:
            meta_tags = {
                'title': _get_model_instance_title(model_instance, model_title_field),
                'h1': default_h1,
                'description': default_description
            }
    else:
        # Getting meta tags for an URL-path.
        try:
            url_path = context['request'].path_info
            meta_tags = MetaTag.objects.get(url=url_path)
            meta_tags.title = meta_tags.title or default_title
            meta_tags.h1 = meta_tags.h1 or default_h1
            meta_tags.description = meta_tags.description or default_description
        except MetaTag.DoesNotExist:
            meta_tags = {
                'title': default_title,
                'h1': default_h1,
                'description': default_description
            }
    return {'meta_tags': meta_tags}


@register.simple_tag(takes_context=True)
def meta_tag_h1(context, *args, **kwargs):
    try:
        url_path = context['request'].path_info
        meta_tags = MetaTag.objects.get(url=url_path)
        return meta_tags.h1
    except MetaTag.DoesNotExist:
        return ''
