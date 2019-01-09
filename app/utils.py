# -*- coding: ascii -*-
"""
app.utils
~~~~~~~~~

Utils. for the application.
"""

import re
import unicodedata
from functools import partial
from Levenshtein import distance

__all__ = [
    'parse_db_uri',
    'parse_citations',
    'parse_doi',
    'normalize',
    'doi_normalize',
    'matching'
]


# Find citations from text
find_citations = [
    # APA style
    re.compile(
        (
            r'((?#authors)[\w-]{2,}(?: *,(?: *[A-Z]\.)+|(?: +[\w-]+)+)?'
            r'(?: *,(?: *(?:&|\.{3}))? *[\w-]{2,}(?: *,(?: *[A-Z]\.)+|(?: +[\w-]+)+)?)*(?:(?<=\.)|(?<!\.) *\.)'
            r'(?#date) *\( *\d{4}(?: *, *\w+(?: +\d+(?: *- *\d+)?)?)? *\) *\.'
            r'(?#title)[^\n]+(?:(?<=\.)|(?<!\.)\.)'
            r'(?#journal|location)(?<=\.)(?:[^\n]+?(?=, *\d+ *\([\w-]+\)|, *\w+(?:-\w+)? *\.|\.)'
            r'(?#journal:volume)(?:, *\d+ *\([\w-]+\))?(?#journal:pages)(?:, *\w+(?:-\w+)?)? *\.)?'
            r'(?#doi)(?: *(?:doi: *|http://dx\.doi\.org/)[^\s]+)?)'
        ),
        flags=re.IGNORECASE + re.DOTALL
    ).findall,

    # AMA style
    re.compile(
        (
            r'(?:\n|^)'
            r'((?#authors)(?:[\w-]{2,}(?: +[A-Z]+)?(?: *, *[\w-]{2,}(?: +[A-Z]+)?)* *\.)?'
            r'(?#title) *\w{2}[^\n;.]+\.(?#title:journal|conference) *\w{2}[^\n;.]+'
            r'(?:(?#journal)\.(?#date) *(?:[a-z]{3}(?: +\d{1,2})? *, *)?\d{4}'
            r'(?#volume)(?: *;(?: *\d+)?(?: *\( *[\w-]+ *\))?)?'
            r'(?#page)(?: *: *\w+(?: *- *\w+)?)?|(?#conference)'
            r'(?#date); *(?:[a-z]{3}(?: +\d+(?: *- *(?:\d+|[a-z]{3} +\d+))?)? *, *)?\d{4}'
            r'(?#location)(?: *; *\w{2}[^\n;.]+)?) *\.'
            r'(?#doi)(?: *(?:doi: *|http://dx\.doi\.org/)[^\s]+)?)'
        ),
        flags=re.IGNORECASE + re.DOTALL
    ).findall
]

# Parse DOI in citation
parse_doi = re.compile(
    r'(?:doi: *|http://dx\.doi\.org/)([^\s]+)',
    flags=re.IGNORECASE
).findall


def parse_citations(text):
    """Parse text into list of citations"""
    ret = []
    for finder in find_citations:
        ret.extend(finder(text))
    return ret


def parse_db_uri(conf):
    """
    Parse input database config into database URI format

    :param conf:    input database config
    :type conf:     dict
    :return:        string of database config in URI format
    :rtype:         str
    """

    # Input config must be a dict
    assert isinstance(conf, dict)

    # Key 'dbname' is required in config
    if 'dbname' not in conf:
        raise ValueError('No database specified')

    # Read and parse config
    dbname = str(conf['dbname'])
    host = str(conf.get('host', '127.0.0.1') or '127.0.0.1')
    port = str(conf.get('port', ''))
    user = str(conf.get('user', ''))
    passwd = str(conf.get('passwd', ''))
    driver = str(conf.get('driver', 'postgresql')).lower() or 'postgresql'

    if user and passwd:
        user = '%s:%s@' % (user, passwd)
    elif user:
        user = '%s@' % user
    elif passwd:
        raise ValueError('No user with that password')

    if port:
        if not port.isdigit():
            raise ValueError('Database port must be a number')
        host = '%s:%s' % (host, port)

    # Return parsed config in URI format
    return '{}://{}{}/{}'.format(driver, user, host, dbname)


def normalize(text, case=True, spaces=True, unicode=True):
    """
    Normalize text

    :param text:    input text
    :type text:     str
    :param case:    normalize to lower case, default is True
    :type case:     bool
    :param spaces:  normalize spaces, default is True
    :type spaces:   bool
    :param unicode: convert unicode characters to ascii, default is True
    :type unicode:  bool
    :return:        normalized text
    :rtype:         str
    """

    # Normalize unicode
    if unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()

    # Normalize case
    if case:
        text = text.lower()

    # Normalize spaces
    if spaces:
        text = ' '.join(text.split())

    # Return normalized text
    return text


# Normalize DOI
doi_normalize = partial(normalize, case=True, spaces=False, unicode=False)


def mark_exact(citation):
    """Highlight exact matches"""
    return '<mark class="exact-match">%s</mark>' % citation


def mark_approx(citation):
    """Highlight approximate matches"""
    return '<mark class="approx-match">%s</mark>' % citation


def doi_matched(citation, dois):
    """
    Parse DOI value from the input citation, check if the DOI value exists in the list of DOIs

    :param citation:    input citation
    :type citation:     str
    :param dois:        input list of DOIs
    :type dois:         set or list or tuple
    :return:            True if it exists, else False
    :rtype:             bool
    """

    # Parse DOI in citation
    doi = parse_doi(citation)

    # DOI found
    if doi:
        return doi_normalize(doi[0]) in dois

    # DOI not found
    return False


def ld_matched(citation, citations, max_distance):
    """
    Is there a match that is less than max_distance?
    Minimum Levenshtein distance between the citation and 
    a list of available citations or None. 

    :param citation:        input citation
    :type citation:         str
    :param citations:       list of available citations being matched against
    :type citations:        list or tuple
    :param max_distance:    maximum edit distance
    :type max_distance:     int
    :return:                minimum edit distance number if match found, else None
    :rtype:                 int or None
    """

    # Create a generator of edit distance numbers
    distances = (distance(normalize(citation), normalize(c.value)) for c in citations)

    # Filter distance numbers based on input max_distance
    candidates = filter(lambda x: x <= max_distance, distances)

    # Return min number of filtered distance numbers, or None
    return min(candidates, default=None)


def matching(citation, dois, citations, max_distance):
    """
    Main function for matching citation. Returns markup based
    on result from matching.

    :param citation:        citation for doing matching
    :type citation:         str
    :param dois:            list of DOIs
    :type dois:             set or list or tuple
    :param citations:       list of available citations
    :type citations:        list or tuple
    :param max_distance:    maximum edit distance
    :type max_distance:     int
    :return:                markup text for input citation
    :rtype:                 str
    """

    # Match using DOI
    if doi_matched(citation, dois):
        return mark_exact(citation)

    # Match using Levenshtein Edit Distance
    else:
        min_distance = ld_matched(citation, citations, max_distance)
        if min_distance is None:
            return citation  # no match found
        elif min_distance == 0:
            return mark_exact(citation)  # exact match
        else:
            return mark_approx(citation)  # approx. match
