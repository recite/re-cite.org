# -*- coding: ascii -*-
"""
styles.parsers
~~~~~~~~~~~~~~

Parsers for citation styles.
"""

import re
from datetime import datetime

__all__ = ['parse_author', 'parse_year', 'parse_date', 'parse_page']

# Find author name
find_author = re.compile(r'([A-Za-z-]{2,})(, ?([A-Z]+))?').match

# Find initials in author name
find_initial = re.compile(r'([A-Z])').findall

# Find year in string
find_year = re.compile(r'([0-9]{4}|[a-zA-Z]{3}-([0-9]{2,4}))').findall

# Find month in string
find_month = re.compile(r'([a-zA-Z]{3})').findall

# Find day or day range in string
find_day = re.compile(r'\b(\d{1,2}(?:-\d{1,2})?)\b(?!$)').findall


def parse_author(text, surname_sep=' ', initial_sep='', initial_suffix=''):
    """
    Parse input text and return list of authors.

    :param text:           input text to parse
    :param surname_sep:    separation between surname and initials
                           of each author found
    :param initial_sep:    separation among initials
    :param initial_suffix: suffix to be appended to each initial
    :return:               list of author names parsed from text
    """

    authors = []
    for found in (find_author(i.strip()) for i in text.split(';')):
        if found:
            surname, _, initials = found.groups()
            if initials:
                initials = initial_sep.join(i + initial_suffix
                                            for i in find_initial(initials))
                authors.append(surname_sep.join((surname.capitalize(), initials)))
                continue
            authors.append(surname.capitalize())
    return authors


def parse_year(datestring):
    """
    Parse input text and return year string in 4-digit format.

    :param datestring: input text to parse
    :return:           4-digit year or empty
    """

    year = ''

    if datestring and datestring.isdigit():
        if len(datestring) in (2, 4):
            year = datestring

    elif datestring:
        try:
            found = find_year(datestring)[0]
        except IndexError:
            pass
        else:
            if found[0].isdigit():
                year = found[0]
            elif found[-1].isdigit():
                year = found[-1]

    # Verify year
    if year:
        fmt = '%Y' if len(year) == 4 else '%y'
        try:
            dp = datetime.strptime(year, fmt)
        except ValueError:
            pass
        else:
            cur_year = datetime.now().year
            if dp.year > cur_year:
                dp = dp.replace(year=dp.year - 100)
            year = str(dp.year)

    return year


def parse_date(datestring):
    """
    Parses input datestring and returns date in correct format.

    :param datestring: input datestring to parse
    :return:           parsed date or empty
    """

    def day_format(daystring):
        """Returns 2-digit of day"""
        f = lambda x: '{:02d}'.format(int(x.strip()))
        if '-' in daystring:
            return '-'.join(f(i) for i in daystring.split('-') if i.strip())
        return f(daystring)

    date = ''
    months = [m.capitalize() for m in find_month(datestring)]
    if months:
        days = [day_format(d) for d in find_day(datestring)]
        if days:
            date += '-'.join('{} {}'.format(m, d) for m, d in zip(months, days))
        else:
            date += '-'.join(months)

    year = parse_year(datestring)
    if year:
        date += '{}{}'.format(', ' if date else '', year)

    return date


def parse_page(begin_page, end_page):
    """
    Parses and returns page range from begin to end.

    :param begin_page: begining page number
    :param end_page:   ending page number
    :return:           page range or empty string
    """

    if begin_page:
        if end_page and end_page != '+':
            return '%s-%s' % (begin_page, end_page)
        return begin_page
    return ''
