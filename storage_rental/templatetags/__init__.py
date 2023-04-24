from django import template
from .media_tags import media


register = template.Library()
register.simple_tag(media)
