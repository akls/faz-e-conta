from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(key, str) and key.endswith("_id"):
        return dictionary.get(key, "") if dictionary.get(key, "") != None else "Aluno"
    if isinstance(key, str) and key.startswith("hora_"):
        return dictionary.get(key, "") if dictionary.get(key, "") != None else key
    return dictionary.get(key, "")

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new).title()