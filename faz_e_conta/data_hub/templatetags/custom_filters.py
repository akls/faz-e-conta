from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if key.endswith("_id"):
        print(key,"\n\n")
        return dictionary.get(key, "") if dictionary.get(key, "") != None else "Aluno"
    return dictionary.get(key, "")

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new).title()