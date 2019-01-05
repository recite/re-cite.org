# -*- coding: ascii -*-
"""
styles.parsers
~~~~~~~~~~~~~~

Parsers for citation styles.
"""

import re
from datetime import datetime

__all__ = ['parse_author', 'parse_year']

# Find author name
find_author = re.compile(r'([A-Za-z-]{2,})(, ?([A-Z]+))?').match

# Find initials in author name
find_initial = re.compile(r'([A-Z])').findall

# Find year in string
find_year = re.compile(r'([0-9]{4}|[a-zA-Z]{3}-([0-9]{2,4}))').findall


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
    :return:     4-digit year or empty if not found
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
