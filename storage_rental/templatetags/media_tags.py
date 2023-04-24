from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def media(file_path):
    return '{}{}'.format(settings.MEDIA_URL, file_path)
