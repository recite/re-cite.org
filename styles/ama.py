# -*- coding: ascii -*-
"""
styles.ama
~~~~~~~~~~

Generate AMA style for article.
"""

from types import SimpleNamespace
from . import parse_author, parse_date, parse_year

__all__ = ['AMA']

CONFERENCE_PREFIX = 'In:'


class AMA:
    def __init__(self, **kwargs):
        self._f = SimpleNamespace(**kwargs)

    @property
    def _authors(self):
        authors = parse_author(self._f.author)
        if len(authors) > 6:
            authors = authors[:3] + ['et al']
        authors = ', '.join(authors)
        if self._f.group_author:
            if authors:
                authors += '; '
            authors += self._f.group_author.title()
        return authors

    @property
    def _title(self):
        if self._f.article_title:
            return self._f.article_title.capitalize()
        return ''

    @property
    def journal(self):
        return ''

    @property
    def conference(self):
        conf = '; '.join(
            i for i in (
                self._f.conf_title,
                parse_date(self._f.conf_date),
                self._f.conf_location) if i)

        if conf:
            conf = '%s %s' % (CONFERENCE_PREFIX, conf)

        return '. '.join(i for i in (self._authors, self._title, conf) if i)
