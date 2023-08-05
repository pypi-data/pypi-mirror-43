# Shakespear

Use Python to write different display file types (html, markdown), and transform
common python data structures to comparable structures in a given file type _(list in python
to a \<table /> in html, for example)_

## Setup
You can use pip to install shakespear:

```pip install shakespear```

## HTML

Use python functions to create an html body, which can be attached to emails as
the message content (or for any other use one might have for html)

#### Basic Usage
The functions all simply add to the existing html you've generated, so if
you use the same instance across multiple functions it'll append new html.
When you're finished writing your html, just use the `generate` function
to get back your brand new html text.

For example:

```
from shakespear import HtmlWriter

h = HtmlWriter()
data = [
    {'first_name': 'Sam', 'last_name': 'Winchester', 'mood': 'Moody'},
    {'first_name': 'Dean', 'last_name': 'Winchester', 'mood': 'Gruff'},
    {'first_name': 'Cas', 'last_name': 'N/A', 'mood': 'Confused'}
]

h.dict_table(data).generate()
```

Easy as that, you'll have a nice html table that looks like

| first_name | last_name | mood |
| :-:|:-:|:-:|
|Sam| Winchester | Moody |
| Dean | Winchester | Gruff |
| Cas | N/A | Confused |

There are a bunch of other html object functions (table, div, ul, etc) that can
be chained OR written sequentially, or any combination of chaining and new lines
, there's no difference in function it just depends on  your style preference,
or what seems easier to read:

```
h.header('My data').br().hr().ul(data).br().generate()
```

OR

```
h.header('My data')
h.br().hr()
h.ul(data)
h.br()
h.generate()
```

both do the same thing, and generate wil return the same html text.

## Markdown

Use python to create markdown text. My initial use case for this was to generate
automatic change logs for a repo.

#### Basic Usage
Like to html writer, you can chain functions or use them seperatly, `generate`
returns markdown text.

For example:

```
from shakespear import MarkdownWriter

m = MarkdownWriter()
data = [
    {'commiter': 'Richard', 'type': 'Bug Fix', 'title': 'Fix video compression'},
    {'commiter': 'Gilfoyle', 'type': 'New Feature', 'title': 'Add new chat'},
    {'commiter': 'Dinesh', 'type': 'Refactor', 'title': 'Update chat style'}
]

m.dict_table(data).generate()
```

This will give you (in markdown) this table

| commiter | type | title |
| :-:|:-:|:-:|
|Richard| Bug Fix | Fix video compression |
| Gilfoyle | New Feature | Add new chat |
| Dinesh | Refactor | Update chat style |
