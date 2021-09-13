from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='area_cols')
def area_cols(value, arg):
    return value.as_widget(attrs={'cols': arg})

@register.filter(name='area_rows')
def area_rows(value, arg):
    return value.as_widget(attrs={'rows': arg})