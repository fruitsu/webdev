from django import template
import datetime
from django import template


register = template.Library()


def com_many(numb):
    try:
        res = ' комментари'
        if (numb >= 5 and numb <= 20) or (numb % 10 >= 5 and numb % 10 <= 9) or numb % 10 == 0:
            res = str(numb) + res + 'ев'
        elif numb % 10 == 1:
            res = str(numb) + res + 'й'
        elif numb % 10 >= 2 and numb % 10 <= 4:
            res = str(numb) + res + 'я'
        return res
    except:
        return ""


@register.filter(name='max_len')
def max_len(val, max):
    try:
        return val[:max] + (len(val) > max and "..." or "")
    except:
        return ""


register.filter('com_many', com_many)


@register.simple_tag(takes_context=True, name="python_time")
def current_time(context, format_string, *args, **kwargs):
    for i in args:
        print(i)
    for k in kwargs:
        print(k, " - ", kwargs[k])
    return datetime.datetime.strftime(datetime.datetime.now(), format_string)


@register.inclusion_tag('blog/includes/btn.html')
def show_results(txt):
    return {'txt': txt}


class MultipleNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, var1, var2, nodelist_true, nodelist_false):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        val1 = self.var1.resolve(context, ignore_failures=True)
        val2 = self.var2.resolve(context, ignore_failures=True)
        if val1 % val2 == 0:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


@register.tag
def multiply(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('Если', end_tag))
    token = parser.next_token()
    if token.contents == 'Если':
        nodelist_false = parser.parse((end_tag,))
        parser.next_token()
    else:
        nodelist_false = ""
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])

    return MultipleNode(val1, val2, nodelist_true, nodelist_false)


class MultipleNode2(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        if len(self.nodelist) == 0:
            return ""
        for i in self.nodelist:
            if i[0]:
                if i[1] is not None and i[2] is not None:
                    val1 = i[1].resolve(context, ignore_failures=True)
                    val2 = i[2].resolve(context, ignore_failures=True)
                    if val1 % val2 == 0:
                        return i[0].render(context)
                else:
                    return i[0].render(context)
        return ""


@register.tag
def кратность(parser, token):
    bits = list(token.split_contents())
    nodelist = []
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'конец' + bits[0]
    nodelist.append((parser.parse(('ИфЕсли', 'Если', end_tag)), parser.compile_filter(bits[1]), parser.compile_filter(bits[2])))

    token = parser.next_token()

    while token:
        bits = list(token.split_contents())
        if len(bits) == 3 and bits[0] == 'ИфЕсли':
            nodelist.append((parser.parse(('ИфЕсли', 'Если', end_tag)), parser.compile_filter(bits[1]), parser.compile_filter(bits[2])))
        else:
            if len(bits) == 1 and bits[0] == 'Если':
                nodelist.append((parser.parse((end_tag,)), None, None))
            else:
                nodelist.append(("", None, None))
                break

        try:
            token = parser.next_token()
        except IndexError:

            token = False

    return MultipleNode2(nodelist)


@register.filter(name='valid_url')
def valid_url(value, arg):
    #url = 'http://'
    #if url.startswith('http://'):
    #    pass
    #else:
        return '{scheme}://'.format(scheme='http')
