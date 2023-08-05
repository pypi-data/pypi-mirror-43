class MarkdownWriter:

    def __init__(self):
        self.markdown = ""

    def _header(self, val, size=1):
        if size > 6:
            size = 6

        return "{} {}".format("#" * size, val)

    def _italic(self, val):
        return "_{}_ ".format(val)

    def _bold(self, val):
        return "**{}** ".format(val)

    def _bullet(self, val):
        return "+ {}\n".format(val)

    def _numbered_item(self, val, i):
       return "{}. {}\n".format(i, val)

    def _link(self, link):
        return "[{}] ".format(link)

    def _link_text(self, val):
        return "({}) ".format(val)

    def _list_item(self, val, i):
        self.markdown += self._numbered_item(val, i)

    def n(self):
        self.markdown += '\n\n'
        return self

    def t(self):
        self.markdown += '\t'
        return self

    def italic(self, val):
        self.markdown += self._italic(val)
        return self

    def bold(self, val):
        self.markdown += self._bold(val)
        return self

    def bullet(self, val):
        self.markdown += self._bullet(val)
        return self

    def header(self, val, size=1):
        self.markdown += self._header(val, size)
        return self

    def text(self, val):
        self.markdown += f"{val} "
        return self

    def ordered_list(self, iterable):
        for i, val in enumerate(iterable):
            self._list_item(val, i)

        return self

    def unordered_list(self, iterable):
        for val in iterable:
            self.bullet(val)

        return self

    def labeled_link(self, url, text):
        self.markdown += "{}{}".format(self._link(url), self._link_text(text))
        return self

    def unlabeled_link(self, url):
        self.markdown += "{}".format(self._link(url))
        return self

    def link(self, url, text=None):
        self.unlabeled_link(url) if text is None else self.labeled_link(url, text)
        return self

    def generate(self, title=None):
        title = 'CHANGELOG' if title is None else f'{title.upper()}_CHANGELOG.md'
        with open(title, 'w') as f:
            f.write(self.markdown)