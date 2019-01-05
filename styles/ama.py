# -*- coding: ascii -*-
"""
styles.ama
~~~~~~~~~~

Generate AMA style for article.
"""

from types import SimpleNamespace
from . import parse_author

__all__ = ['AMA']


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
    def journal(self):
        return ''

    @property
    def conference(self):
        return ''
