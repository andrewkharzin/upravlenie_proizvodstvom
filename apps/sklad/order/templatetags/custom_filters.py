from django import template

register = template.Library()

@register.filter
def initials(name):
    parts = name.split()
    initials = [part[0] + '.' for part in parts[1:]]
    return parts[0] + ' ' + ' '.join(initials)
