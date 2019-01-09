# -*- coding: ascii -*-
"""
styles.ama
~~~~~~~~~~

Generate AMA style for article.
"""

from types import SimpleNamespace
from .wos import WOS
from .parsers import parse_author, parse_date, parse_year, parse_page

__all__ = ['AMA']

CONFERENCE_PREFIX = 'In: '


class AMA:
    def __init__(self, **kwargs):
        self._f = SimpleNamespace(**kwargs)
        self._wos = WOS()
        self._journal = None
        self._conference = None

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
    def _journal_title(self):
        name = self._f.pub_name
        if name:
            return self._wos.abbreviate(name) or name
        return ''

    @property
    def journal(self):
        if self._journal is None:
            # Generate volume and issue
            vol = ''
            if self._f.volume:
                vol += self._f.volume
            if self._f.issue:
                vol += '(%s)' % self._f.issue

            # Generate page range
            page = parse_page(self._f.begin_page, self._f.end_page)

            # Generate year or date
            year = ''
            if self._f.pub_year or self._f.pub_date:
                if vol:
                    year = parse_year(self._f.pub_year)
                else:
                    year = parse_date(self._f.pub_date, self._f.pub_year)

            # Construct last part
            last = year
            if vol:
                last += '{}{}'.format(';' if last else '', vol)
            if page:
                last += '{}{}'.format(':' if last else '', page)

            # Construct journal citation
            journal = '. '.join(
                i for i in (
                    self._authors,
                    self._title,
                    self._journal_title,
                    last
                ) if i
            )

            # Store journal citation
            self._journal = journal + '.' if not journal.endswith('.') else journal

        # Return value
        return self._journal

    @property
    def conference(self):
        if self._conference is None:
            # Construct conference info
            conf = '; '.join(
                i for i in (
                    self._f.conf_title,
                    parse_date(self._f.conf_date),
                    self._f.conf_location
                ) if i
            )

            # Construct conference citation
            if conf:
                conf = '. '.join(
                    i for i in (
                        self._authors,
                        self._title,
                        '%s%s' % (CONFERENCE_PREFIX, conf)
                    ) if i
                )

            # Store conference citation
            self._conference = conf + '.' if not conf.endswith('.') else conf

        # Return value
        return self._conference
