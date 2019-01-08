# -*- coding: ascii -*-
"""
styles.apa
~~~~~~~~~~

Generate APA style for article.
"""

from .parsers import parse_author, parse_year, parse_page

__all__ = ['APA']

CONFERENCE_PREFIX = 'Paper presented at '


def gen_author(author, group_author=None):
    """
    Generates authors string in APA format.

    :param author:          input author field, required
    :type author:           str
    :param group_author:    input group_author field, default is None
    :type group_author:     str or None
    :return:                String of authors in APA format
    :rtype:                 str
    """

    authors = parse_author(author, surname_sep=', ',
                           initial_sep=' ', initial_suffix='.')

    if group_author:
        authors.append(group_author.title())

    # Generate and return string of authors in APA format
    if authors:
        if len(authors) > 1:
            if len(authors) > 7:
                sep = '...'
                stop = 6
            else:
                sep = '&'
                stop = -1
            ret = '%s, %s %s' % (', '.join(authors[:stop]), sep, authors[-1])
        else:
            ret = authors[0]
        if not ret.endswith('.'):
            ret += '.'
        return ret

    # Return empty if no author found
    return ''


def gen_date(date, year=None):
    """
    Generates date in APA format (currently outputs only year).

    :param date:    input date, required
    :type date:     str
    :param year:    input year, default is None
    :type year:     str or None
    :return:        date annotation in APA format
    :rtype:         str
    """

    year = parse_year(year) or parse_year(date)
    if year:
        return ' (%s).' % year
    return ''


def gen_title(title, special_issue=None):
    """
    Generates article title in APA format.

    :param title:           original title
    :type title:            str
    :param special_issue:   special issue number of article, default is None
    :type special_issue:    str or None
    :return:                title plus special issue (if any) printed in APA format
    :rtype:                 str
    """

    ret = ''
    if title:
        ret += ' %s' % title.capitalize()
        if special_issue:
            ret += ' [%s]' % special_issue
        if not ret.endswith('.'):
            ret += '.'
    return ret


def gen_journal(title, volume, issue, begin_page, end_page):
    """
    Generates journal (periodical) information in APA format.

    :param title:       journal title
    :type title:        str
    :param volume:      journal volume number
    :type volume:       str
    :param issue:       specific issue number of volume
    :type issue:        str
    :param begin_page:  start page
    :type begin_page:   str
    :param end_page:    end page
    :type end_page:     str
    :return:            journal info in APA format
    :rtype:             str
    """

    ret = ''
    if title:
        ret += ' %s' % title.title()
        if volume and issue:
            ret += ', %s(%s)' % (volume, issue)
        elif volume:
            ret += ', %s' % volume
        elif issue:
            ret += ', (%s)' % issue
        if begin_page:
            ret += ', %s' % parse_page(begin_page, end_page)
        if not ret.endswith('.'):
            ret += '.'
    return ret


def gen_doi(doi):
    """Generates DOI number in APA format using original DOI."""
    return ' doi:%s' % doi if doi else ''


def gen_conf(title, location):
    """
    Generates conference info in APA format.

    :param title:    conference title
    :param location: location where conference was conducted
    :return:         conference info (str)
    """

    conf = ''
    if title or location:
        conf += ' %s' % CONFERENCE_PREFIX

        if title:
            conf += title
            if location:
                conf += ', '

        if location:
            conf += location

        if not conf.endswith('.'):
            conf += '.'

    return conf


class APA:
    _fmt = '{author}{date}{title}{last}'
    _fmt_no_author = '{title}{date}{last}'

    def __init__(self, **kwargs):
        self.journal = ''
        self.conference = ''

        has_author = bool(kwargs.get('author') or kwargs.get('group_author'))
        has_journal = bool(kwargs.get('article_title'))
        has_conference = bool(kwargs.get('conf_title'))

        fmt = self._fmt if has_author else self._fmt_no_author
        author = gen_author(kwargs.get('author'), kwargs.get('group_author'))

        if has_journal:
            self.journal = fmt.format(
                author=author,
                date=gen_date(kwargs.get('pub_date'), kwargs.get('pub_year')),
                title=gen_title(kwargs.get('article_title'),
                                kwargs.get('special_issue')),
                last=gen_journal(kwargs.get('pub_name'), kwargs.get('volume'),
                                 kwargs.get('issue'), kwargs.get('begin_page'),
                                 kwargs.get('end_page'))
            ).strip()

        if has_conference:
            self.conference = fmt.format(
                author=author,
                date=gen_date(kwargs.get('conf_date')),
                title=gen_title(kwargs.get('article_title')),
                last=gen_conf(kwargs.get('conf_title'), kwargs.get('conf_location'))
            ).strip()
