# picot

Picot is a library to read, select and extract information from RSS feeds.

## Installation

You can install it using `pip install` as usual:
```bash
pip install picot
 ```

## Usage

### As a module

Picot is intended to be used mostly as a module, providing with some RSS feed goodies.
```python
import picot.feed

entries = picot.feed.Feed(url)
for entry in entries:
    print(entry['title'])
```

#### Filter

In order to make filtering easier, you can provide `Feed` with a function determining what entries are selected:
```python
entries = picot.feed.Feed(url, filter_func=lambda x: x['title'].startswith('How to'))
```

#### Formatting

It provides with a formatting function, defining how entries are represented:
```python
entries = picot.feed.Feed(url, format_func=lambda x: '{} {}'.format(x['title'], x['link']))
```

### As a command

While intended to be used as a library, Picot can be invoked as a command line tool to get the titles of the entries in an RSS:
```bash
$ picot <RSS URL>
```
