import re

from .base_css import BASIC_CSS_CLASSES


class HtmlWriter:
    """
    Html Writing object to create html using python. Mostly for formatting emails, but I guess
    You can use it to generate html for other purposes too.

    :param: kwargs (for any function) can contain these elements:
        { 'classes': List of Strings
          'bold': Boolean
          'italic': Boolean
          'strong': Boolean
        }
    """

    def __init__(self, styles=None, **kwargs):
        """
        :param styles: Array of style strings
        :param kwargs:
        """
        self.styles = [BASIC_CSS_CLASSES]
        self.html_body = ""
        self.html_head = ""

        if styles:
            self.styles.extend(styles)

    # ====================== #
    #    Helper Functions    #
    # ====================== #
    # Functions which either return tag strings formated with content, or help parse info like classes
    # and attributes and then add it to tags


    # ========================================== #
    #    Parsers and tag formatting functions    #
    # ========================================== #
    # Turn arrays of strings like classes or styles into tags, or strings to be used in tags. Also some write
    # functions (basically just setters)

    def _write_head(self, val):
        self.html_head += val

    def _write_body(self, val):
        self.html_body += val

    def _parse_html_head(self, head_groups):
        for head in head_groups:
            head = head.replace('<head>', '').replace('</head>', '')
            self._write_head(head)

    def _parse_html_body(self, body_groups):
        for body in body_groups:
            body = body.replace('<body>', '').replace('</body>', '')
            self._write_body(body)

    def _parse_styles(self):
        return "\n".join(["<style>{style_sheet}</style>".format(style_sheet=style_sheet) for style_sheet in self.styles])

    def _add_text_tags(self, val, **kwargs):
        # text could have all of these (don't know what <bold><strong> looks like but technically it's ok to do)
        if kwargs.get('bold') == True:
            val = self._bold(val)
        if kwargs.get('italic') == True:
            val = self._italicize(val)
        if kwargs.get('strong') == True:
            val = self._strong(val)

        return val

    def _add_classes(self, **kwargs):
        if kwargs.get('classes'):
            return "class='{}'".format(" ".join([class_name for class_name in kwargs.get('classes')]))
        else:
            return ""

    def _iterator_value_handler(self, iterate, key):
        val = iterate.get(key, self._italicize('{} not found'.format(key)))
        if val is None:
            return self._italicize("No {} Found".format(key))
        else:
            return val


    # ============================== #
    #    tag generation functions    #
    # ============================== #
    # return tags with classes and all formatting (bold, italic, etc.)

    def _generate_tag(self, tag, val, **kwargs):
        return "<{tag} {class_name}>{val}</{tag}>".format(tag=tag,
                                                          class_name=self._add_classes(**kwargs),
                                                          val=self._add_text_tags(val, **kwargs))

    def _bold(self, val):
        return self._generate_tag('b', val)

    def _italicize(self, val):
        return self._generate_tag('i', val)

    def _strong(self, val):
        return self._generate_tag('strong', val)

    def _span(self, val, **kwargs):
        return self._generate_tag('span', val, **kwargs)

    def _p(self, val, **kwargs):
        return self._generate_tag('p', val, **kwargs)

    def _div(self, contents, **kwargs):
        return "<div {class_name}>{contents}</div>"\
               .format(contents=contents, class_name=self._add_classes(**kwargs))

    def _header(self, size, val, **kwargs):
        # HTML only has headers 1-6
        if size < 1 or size > 6:
            size = 6
        return self._generate_tag('h{size}'.format(size=str(size)), val, **kwargs)

    def _li(self, val, **kwargs):
        return self._generate_tag('li', val, **kwargs)

    def _ul(self, lis, **kwargs):
        return self._generate_tag('ul', ''.join([self._li(li, **kwargs) for li in lis]), **kwargs)

    def _td(self, val, **kwargs):
        return self._generate_tag('td', val, **kwargs)

    def _tr(self, tds, **kwargs):
        return self._generate_tag('tr', ''.join([self._td(td, **kwargs) for td in tds]), **kwargs)

    # ===================== #
    # User facing functions #
    # ===================== #
    # These functions are what should be called when using this class. Helper functions
    # above can be used freely too, for creating more custom html, but for the basics, these
    # plus a css string will be sufficient


    # ====================== #
    # Tables, Tr's, and Td's #
    # ====================== #
    # Table functions, including dict and list based table creation

    # User facing in case someone wants to create super customized table rows and table cells, easy enough
    # to create the basic string for a table and then format it with custom td's and tr's
    def td(self, val, **kwargs):
        self.html_body += self._td(val, **kwargs)
        return self

    def tr(self, tds, **kwargs):
        self.html_body += self._tr(tds, **kwargs)
        return self

    def dict_table(self, iterator, caption='', **kwargs):
        """
        This works similarly to the csv.DictWriter

        :param iterator: a dict object of data
        :return:
        """
        headers = [key for key, value in iterator[0].items()]
        self.html_body += "<table {class_name}>{caption}<thead>{headers}</thead>"\
                          .format(caption=caption,
                                  headers=self._tr(headers, **{'bold':True}),
                                  class_name=self._add_classes(**kwargs))

        for iterate in iterator:
            self.tr([self._iterator_value_handler(iterate, key) for key in headers])

        self.html_body += "</table>"
        return self


    def list_table(self, iterator, caption='', **kwargs):
        """
        This works similarly to the csv.Writer, no headers needed

        :param iterator: a list object of data
        :return:
        """
        self.start_div(classes=['table-container'])
        self.html_body += "<table {class_name}>{caption}" \
            .format(caption=caption,
                    class_name=self._add_classes(**kwargs))

        for iterate in iterator:
            self.tr([self._td(val) for val in iterate ])

        self.html_body += "</table>"
        self.end_div()
        return self


    # ======================= #
    #     Basic  Elements     #
    # ======================= #
    # Elements like headers and simple lists

    def header(self, size, val, **kwargs):
        self.html_body += self._header(size, val, **kwargs)
        return self

    def ul(self, list_values, **kwargs):
        self.html_body += self._ul(list_values, **kwargs)
        return self

    def span(self, val, **kwargs):
        self.html_body += self._span(val, **kwargs)
        return self

    def hr(self):
        self.html_body += "<hr>"
        return self

    def br(self):
        self.html_body += "<br>"
        return self

    # ===================== #
    #          Divs         #
    # ===================== #
    # Divs can be created either with content inside of them, or by starting a div, calling
    # some of these writer functions, and then closing the div

    def div(self, contents, **kwargs):
        self.html_body += self._div(contents, **kwargs)
        return self

    def start_div(self, **kwargs):
        self.html_body += "<div {class_name}>".format(class_name=self._add_classes(**kwargs))
        return self

    def end_div(self):
        self.html_body += "</div>"
        return self

    # ============================ #
    #       Custom Components      #
    # ============================ #
    # Custom html components

    def text_div(self, text, **kwargs):
        self.start_div(**kwargs)
        if 'classes' in kwargs:
            kwargs['classes'].append('small-padding')
        else:
            kwargs['classes'] = ['small-padding']
        self.span(text, **kwargs)
        self.end_div()
        return self

    def dict_table_container(self, header, iterator, status='info'):
        self.header(3, header, classes=['table-header table-header-{}'.format(status)])
        self.start_div(classes=['table-container'])
        self.dict_table(iterator)
        self.end_div()
        return self

    def list_table_container(self, header, iterator, status='info'):
        self.header(3, header, classes=['table-header table-header-{}'.format(status)])
        self.start_div(classes=['table-container'])
        self.list_table(iterator)
        self.end_div()
        return self

    def text_badge(self, text, status='info'):
        self.div(contents=text, classes=['background-{}'.format(status)])
        return self

    def html(self, html):
        """
        function to add a custom built html string onto this html body
        :param html: html string (string of html elements)
        :return:
        """

        # Don't want to add extra html tags
        html = html.replace('<html>', '').replace('</html>', '')

        # Assume that if body tag isn't specified (or head) the string is just tags to be added
        # to the current body
        if '<body>' in html or '<head>' not in html:
            head = re.findall(r'<head>.*<\/head>', html, re.S)
            self._parse_html_head(head)
            body = re.findall(r'<body>.*<\/body>', html, re.S)
            self._parse_html_body(body)
        else:
            self._write_body(html)




    def generate(self):
        html = """
                    <html>
                    <head>
                        {head}
                        {style_sheet}
                    </head>    
                    </body>
                        {body}
                    </body>    
                    </html>    
                """.format(style_sheet=self._parse_styles(), head=self.html_head, body=self.html_body)
        return html