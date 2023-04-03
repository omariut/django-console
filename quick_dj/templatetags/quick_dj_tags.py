from django import template
from quick_dj.utils import get_data_from_file
register = template.Library()

@register.filter
def get_options_with_default_values(value):
    fields = get_data_from_file('fields.json')
    field_options= fields.get(value,[])
    common_options=fields.get("Common",[])
    return field_options + common_options

@register.filter
def get_all_fields(value):
    fields = get_data_from_file('fields.json')
    field_types=list(fields.keys())
    field_types.remove("Common")
    return field_types
