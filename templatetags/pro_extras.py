from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode


register = Library()

IGNORE_METHODS = ['join']


@register.simple_tag
def stringmethod(name, value, first=None, second=None, third=None):
    return make_filter(name)(value, first, second, third)


@stringfilter
def make_filter(name):
    def filter(value, first=None, second=None, third=None):
        args = [first, second, third]
        method = getattr(force_unicode(value), name)

        while True:
            try:
                return method(*args)
            except TypeError:
                args.pop(len(args) - 1)

    return filter


for name in dir(u''):
    # Ignore all private string methods
    if name.startswith('_'):
        continue

    # Ignore ``join`` method
    if name in IGNORE_METHODS:
        continue

    # Create new template filters for all string methods that not yet added
    # to Django template built-ins
    register.filter(name, make_filter(name))
