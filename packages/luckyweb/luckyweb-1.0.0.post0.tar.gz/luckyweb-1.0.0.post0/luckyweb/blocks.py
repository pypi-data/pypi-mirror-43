import collections
import os
import re


LUCKY_HOME = os.path.dirname(os.path.abspath(__file__))
LUCKY_TEMPLATES = os.path.join(LUCKY_HOME, 'templates')

class TemplateSyntaxError(ValueError):
    """Raised when a template has a syntax error."""
    pass

class CodeBuilder(object):
    INDENT_STEP = 4

    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def __str__(self):
        return "".join(str(c) for c in self.code)

    def add_line(self, line):
        self.code.extend([" " * self.indent_level, line, "\n"])

    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    def indent(self):
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        self.indent_level -= self.INDENT_STEP

    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace

class Template(object):
    '''
    Example:
    >>> html = '<h1> Hello {{ name }} </h1>'
    >>> template = Template(html)
    >>> template.render({'name': 'kk'})
    '''
    def __init__(self, text, *contexts):
        '''
        Arguments:
        - text: html string
        - *contexts: additions function in dict object, it's a option

        Examples:
        >>> html = '<h1> Hello {{ name|upper }} </h1>'
        >>> tpl = Template(html, {'upper': str.upper})
        >>> tpl.render({'name': 'kk'})
        #<h1> Hello KK </h1>
        '''
        self.context = {}
        for context in contexts:
            self.context.update(context)

        self.all_vars = set()
        self.loop_vars = set()

        code = CodeBuilder()

        code.add_line('def render_function(context, do_dots):')
        code.indent()
        vars_code = code.add_section()
        code.add_line('result = []')
        code.add_line('append_result = result.append')
        code.add_line('extend_result = result.extend')
        code.add_line('to_str = str')

        buffered = []
        def flush_output():
            if len(buffered) == 1:
                code.add_line('append_result({})'.format(buffered[0]))
            elif len(buffered) > 1:
                code.add_line('extend_result([{}])'.format(', '.join(buffered)))
            del buffered[:]

        ops_stack = []

        tokens = re.split(r'(?s)({{.*?}}|{%.*?%}|{#.*?#})', text)

        for token in tokens:
            if token.startswith('{#'):
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                buffered.append('to_str({})'.format(expr))
            elif token.startswith('{%'):
                flush_output()
                words = token[2:-2].strip().split()
                if words[0] == 'if':
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", token)
                    ops_stack.append('if')
                    code.add_line('if {}:'.format(self._expr_code(words[1])))
                    code.indent()
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    ops_stack.append('for')
                    self._variable(words[1], self.loop_vars)
                    code.add_line('for c_{} in {}:'.format(words[1], self._expr_code(words[3])))
                    code.indent()
                elif words[0] == 'else':
                    if len(words) != 1:
                        self._syntax_error("Don't understand else", token)
                    if not ops_stack:
                        self._syntax_error('Mismatched ops tag', token)
                    code.dedent()
                    code.add_line('else:')
                    code.indent()
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if not ops_stack:
                        self._syntax_error('Too many ends', token)
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error('Mismatched end tag', end_what)
                    code.dedent()
                else:
                    self._syntax_error("Don't understand tag", words[0])
            else:
                if token:
                    buffered.append(repr(token))

        if ops_stack:
            self._syntax_error('Unmatched action tag', ops_stack[-1])

        flush_output()

        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line('c_{} = context[{}]'.format(var_name, repr(var_name)))

        code.add_line("return ''.join(result)")
        code.dedent()
        self._render_function = code.get_globals()['render_function']

    def _expr_code(self, expr):
        if '|' in expr:
            pipes = expr.split('|')
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = 'c_{}({})'.format(func, code)
        elif '.' in expr:
            dots = expr.split('.')
            code = self._expr_code(dots[0])
            args = ', '.join(repr(d) for d in dots[1:])
            code = 'do_dots({}, {})'.format(code, args)
        elif re.match(r'[_a-zA-Z][_a-zA-Z0-9]*\[[_a-zA-Z0-9:\-]+\]$', expr) and (len(expr.split(':')) <= 3):
            f_name = expr.split('[')[0]
            i_name = expr.split('[')[1].split(']')[0]
            self._variable(f_name, self.all_vars)
            def isinteger(string):
                try:
                    num = int(string)
                except ValueError:
                    return False
                return True
            format_item = lambda x: x if (isinteger(x) or len(x) == 0) else 'c_{}'.format(x)
            i_name = [format_item(item) for item in i_name.split(':')]
            i_name = ':'.join(i_name)
            code = '{}[{}]'.format(self._expr_code(f_name), i_name)
        else:
            self._variable(expr, self.all_vars)
            code = 'c_{}'.format(expr)
        return code

    def _syntax_error(self, msg, thing):
        raise TemplateSyntaxError('{}: {}'.format(msg, repr(thing)))

    def _variable(self, name, vars_set):
        if not re.match(r'[_a-zA-Z][_a-zA-Z0-9]*$', name):
            self._syntax_error('Not a valid name', name)
        vars_set.add(name)

    def render(self, context=None):
        '''
        Argument: context is a dict object, be use to transfer variable to template
        '''
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, *dots):
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value.get(dot, '')
            if callable(value):
                value = value()
        return value

class BaseBlock:
    def __init__(self, tpl_filename):
        self.template = self.load_template(tpl_filename)
        self.args = {}
        self.html = ''

    def __call__(self, variable=None):
        if variable is not None:
            if isinstance(variable, str) or (not isinstance(variable, collections.Iterable)):
                variable = [variable]
            self.args.update({'variable': variable})
            self.html = self.template.render(self.args)
        return self.html

    def load_template(self, filename):
        tpl_path = os.path.join(LUCKY_TEMPLATES, filename)
        with open(tpl_path) as f:
            tpl_str = f.read()
        return Template(tpl_str, {'range': range, 'len': len, 'not': lambda x: not x})

    def __repr__(self):
        return self.html

    def __add__(self, obj):
        return self.html + '\n' + str(obj)
    __radd__ = __add__

    def encode(self, encoding='utf-8'):
        return self.html.encode(encoding)

class HtmlBlock(BaseBlock):
    '''
    Arguments:
    - title: text content of html title element
    - css_urls: css link list
    - js_urls: javascript link list
    '''
    def __init__(self, title='', css_urls=[], js_urls=[]):
        css_urls = css_urls or [
            'https://cdn.staticfile.org/twitter-bootstrap/4.1.0/css/bootstrap.min.css']
        js_urls = js_urls or [
            'https://cdn.staticfile.org/jquery/3.2.1/jquery.min.js',
            'https://cdn.staticfile.org/popper.js/1.12.5/umd/popper.min.js',
            'https://cdn.staticfile.org/twitter-bootstrap/4.1.0/js/bootstrap.min.js']
        super(HtmlBlock, self).__init__('html.tpl')
        self.args.update({'title': title, 'css_urls': css_urls, 'js_urls': js_urls})

class GridBlock(BaseBlock):
    '''
    Arguments:
    - cols_num: container col-sm-num list in bootstrap framwork
    - py: padding y num in bootstrap framework, default is 5
    '''
    def __init__(self, cols_num=[], py=5):
        super(GridBlock, self).__init__('grid.tpl')
        self.args.update({'cols_num': cols_num, 'py': py})

class CardBlock(BaseBlock):
    '''
    Argument:
    - header: header text, default is ''
      {% if header %}
      <div class="card-header" > {{ header }} </div>
      {% endif %}
    '''
    def __init__(self, header=''):
        super(CardBlock, self).__init__('card.tpl')
        self.args.update({'header': header})

class NavbarBlock(BaseBlock):
    '''
    Arguments:
    - left_items: is a list of dicts, [dict(active=True, href='xxx', text='xxx') ... ]
    - right_items: is a list of dicts, [dict(btn=False, href='xxx', text='xxx') ... ]
    - _class: is a html attr, same to class in html
    '''
    def __init__(self, left_items=[], right_items=[], _class='bg-dark navbar-dark'):
        super(NavbarBlock, self).__init__('navbar.tpl')
        self.args.update({'left_items': left_items, 'right_items': right_items, '_class': _class})
        self.html = self.template.render(self.args)

class ImgBlock(BaseBlock):
    '''
    Arugments:
    - src: attr of img tag
    - href: attr of img tag, default '#'
    - alt: attr of img tag, default '#'
    - _class: class of img tag, default 'img-thumbnail'
    '''
    def __init__(self, src, href='#', alt='#', _class='img-thumbnail'):
        super(ImgBlock, self).__init__('img.tpl')
        self.args.update({
            'src': src, 'href': href, 'alt': alt, '_class': _class})
        self.html = self.template.render(self.args)

class HeadBlock(BaseBlock):
    '''
    Arguments:
    - text: text string in head tag
    - head_num: <h{{ head_num }}> ... </h{{ head_num }}>
    - display_num: <h1 class="display-{{ display_num }}"> ...
    - center: type is bool, if center is True, addition <center> tag over head
    '''
    def __init__(self, text, head_num=3, display_num=None, center=False):
        super(HeadBlock, self).__init__('head.tpl')
        self.args.update({
            'text': text, 'head_num': head_num, 'display_num': display_num, 'center': center})
        self.html = self.template.render(self.args)

class PBlock(BaseBlock):
    '''
    Arguments:
    - text: <p>{{ text }}</p>
    - lead: type is bool, if lead is True, add "lead" in tag class
    '''
    def __init__(self, text, lead=False):
        super(PBlock, self).__init__('p.tpl')
        self.args.update({'text': text, 'lead': lead})
        self.html = self.template.render(self.args)

class ABlock(BaseBlock):
    '''
    Arguments:
    - text: <a>{{ text }}</a>
    - href: <a href="{{ href }}"> ...
    - _class: <a class="btn {{ _class }}"> ...
    '''
    def __init__(self, text, href='#', _class="btn-primary"):
        super(ABlock, self).__init__('a.tpl')
        self.args.update({'text': text, 'href': href, '_class': _class})
        self.html = self.template.render(self.args)

class TableBlock(BaseBlock):
    '''
    Arguments:
    - array: 2D list, type of item must be str or block
    - _class: <table class="table {{ _class }}">
    '''
    def __init__(self, array, _class=''):
        super(TableBlock, self).__init__('table.tpl')
        self.args.update({'array': array, '_class': _class})
        self.html = self.template.render(self.args)

class PaginationBlock(BaseBlock):
    '''
    Argument:
    - pages: [dict(active=True, disabled=False, href='http://xxxx', text='xxx'), ...]
      <ul class="pagination" >
        {% for page in pages %}
          {% if page.active %}
        <li class="page-item active"> <a class="page-link" href="{{ page.href }}">{{ page.text }}</a> </li>
          {% else %}
                {% if page.disabled %}
        <li class="page-item disabled"> <a class="page-link" href="{{ page.href }}">{{ page.text }}</a> </li>
            {% else %}
        <li class="page-item"> <a class="page-link" href="{{ page.href }}">{{ page.text }}</a> </li>
            {% endif %}
          {% endif %}
        {% endfor %}
      </ul>
    '''
    def __init__(self, pages=[]):
        super(PaginationBlock, self).__init__('pagination.tpl')
        self.args.update({'pages': pages})
        self.html = self.template.render(self.args)

class ListBlock(BaseBlock):
    '''
    Arguments:
    - _list: [dict(href='xxx', _class='xxx', text='xxx'), ...]
    - _class: <div class="list-group {{ _class }}">
    '''
    def __init__(self, _list=[], _class=''):
        super(ListBlock, self).__init__('list.tpl')
        self.args.update({'_list': _list, '_class': _class})
        self.html = self.template.render(self.args)

class FormBlock(BaseBlock):
    '''
    Arguments:
      <form action="{{ action }}" method="{{ method }}" enctype="{{ enctype }}">
        {% for group in groups %}
        <div class="form-group">
          <label>{{ group.label }}</label>
          <input type="{{ group.type }}" class="form-control" placeholder="{{ group.placeholder }}" name="{{ group.name }}">
              {% if group.text %}
          <small class="form-text text-muted">{{ group.text }}</small>
              {% endif %}
        </div>
        {% endfor %}
        <button type="submit" class="btn btn-primary">{{ submit_text }}</button>
      </form>
    '''
    def __init__(self, action, groups, method='post',
                 enctype='multipart/form-data', submit_text='Submit'):
        super(FormBlock, self).__init__('form.tpl')
        self.args.update({
            'action': action, 'groups': groups, 'method': method,
            'enctype': enctype, 'submit_text': submit_text})
        self.html = self.template.render(self.args)
