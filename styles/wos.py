from abc import ABC
from string import ascii_uppercase
from unicodedata import normalize
from html.parser import HTMLParser
from collections import OrderedDict
from urllib.request import urlopen

ALPHABET = ['0-9'] + [ascii_uppercase[i] for i in range(len(ascii_uppercase))]


def to_ascii(text):
    return normalize('NFKD', text).encode('ascii', 'ignore').decode()


class PageReader(HTMLParser, ABC):
    def __init__(self, data):
        assert isinstance(data, (bytes, str)), data
        super(PageReader, self).__init__()
        self._data = OrderedDict()
        self._key = None
        self._recording = False
        if isinstance(data, bytes):
            data = data.decode()
        self.feed(data)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'dt':
            self._key = None
            self._recording = True

    def handle_endtag(self, tag):
        if tag == 'dd' and self._recording:
            self._recording = False

    def handle_data(self, data):
        if self._recording:
            data = data.strip()
            if self._key is None:
                self._key = data.lower()
                self._data[self._key] = ''
            else:
                self._data[self._key] = data
                self._key = None

    def get(self, key, default=None):
        return self._data.get(key.lower(), default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __getitem__(self, item):
        return self._data[item.lower()]

    def __contains__(self, item):
        return item.lower() in self._data

    def __iter__(self):
        yield from self._data

    def __len__(self):
        return len(self._data)


class WOS:
    url = 'https://images.webofknowledge.com/images/help/WOS/{page}_abrvjt.html'

    def __init__(self):
        self.pages = {k: None for k in ALPHABET}

    def __dataprep(self, journal_title):
        initial = journal_title.strip('"\'')[0]
        page = '0-9' if initial.isdigit() else to_ascii(initial).upper()
        if page in self.pages:
            if self.pages.get(page) is None:
                data = urlopen(url=self.url.format(page=page))
                self.pages[page] = PageReader(data.read())
            return page
        return None

    def abbreviate(self, journal_title):
        page = self.__dataprep(journal_title)
        return self.pages[page].get(journal_title) if page else None
