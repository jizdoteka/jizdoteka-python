from django import template
import re

register = template.Library()

@register.filter
def first_city(queryset):
    return queryset.order_by('order')[0].waypoint.city


@register.filter
def last_city(queryset):
    return queryset.order_by('-order')[0].waypoint.city


@register.filter
def sort_wpts(queryset):
    return queryset.order_by('order')


@register.filter
def pretty_name(queryset):
    return '%s %s [%s]' % (
        queryset.first_name,
        queryset.last_name,
        queryset.username
    )


@register.filter
def get_range(value):
    """
    https://djangosnippets.org/snippets/1357/
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise

r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


@register.filter
def expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments") % token.contents[0]
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError("%r tag at least require one argument") % tag_name

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
