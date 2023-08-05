import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_json_ld(structured_data):
    dumped = json.dumps(structured_data, ensure_ascii=False)
    text = "<script type=application/ld+json>{dumped}</script>".format(dumped=dumped)
    return mark_safe(text)
