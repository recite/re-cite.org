#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
Clean up the database and import data from a CSV file 
which follows a specific predefined data format.

For more information, try:
    ./freshdb.py --help
"""

import os
import re
import csv
import time
from datetime import datetime
from argparse import ArgumentParser
from collections import namedtuple, OrderedDict
from functools import partial
from app import db
from app.models import Article, Citation

# Convention of fields in CSV file
CsvRow = namedtuple('CsvRow', 'author author_full_name group_author article_title pub_name conf_title conf_date \
conf_location researcher_id orcid pub_date pub_year volume issue special_issue begin_page end_page article_number doi \
pubmed_id index')

# Function for refining value of article title field
refine_article_title = partial(re.compile(r'\s*(\(retract(ed|ion)[^()]*\))\s*$', flags=re.IGNORECASE).sub, '')

# Function for parsing list of authors from author field
parse_author = re.compile(r'([A-Za-z-]{2,})(, ?([A-Z]+))?').match

# Function for parsing initials from a name of author
parse_initial = re.compile(r'([A-Z])').findall

# Function for parsing year from date fields
parse_year = re.compile(r'([0-9]{4}|[a-zA-Z]{3}-([0-9]{2,4}))').findall


def get_args(*params):
    """Parses and reads input arguments from command line."""

    parser = ArgumentParser(description='Refresh database by input CSV')
    parser.add_argument('file', metavar='FILE', help='retracted articles file in CSV format')
    args = parser.parse_args(*params)

    # Check file input
    if os.path.isfile(args.file):
        if args.file[-3:] not in ('csv', 'CSV'):
            parser.error('Not a CSV file: %s' % args.file)
    else:
        parser.error('FILE does not exist: %s' % args.file)

    # Return arguments
    return args


def read_csv(file, has_header=True):
    """
    Reads CSV file and returns rows of data

    :param file:        input CSV file path
    :type file:         str
    :param has_header:  does the file have a header? default is True
    :type has_header:   bool
    :return:            rows of data
    :rtype:             list
    """

    with open(file, newline='') as fp:
        rows = []
        data = csv.reader(fp, delimiter=',', quotechar='"')
        header = None
        for row in data:
            if row:
                if header is None:
                    header = row
                    if has_header:
                        continue
                rows.append(CsvRow(*row))
        return rows


def clear_data():
    """Clean-up (truncate) all the data in the database."""

    # Truncate tables
    meta = db.metadata
    sequences = []
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        sequences.append('%s_id_seq' % table.name)
    db.session.commit()

    # Reset sequence numbers
    for seq in sequences:
        db.session.execute('ALTER SEQUENCE %s RESTART WITH 1;' % seq)
    db.session.commit()


def db_init_or_reset():
    """Initialize database if starting afresh. 
    Cleanup if database already exists."""

    if db.engine.has_table(Article.__tablename__):
        clear_data()
    else:
        db.create_all()


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

    authors = []

    # Parse author field
    if author:
        for matched in (parse_author(i.strip()) for i in author.split(';')):
            if matched:
                lastname, _, initials = matched.groups()
                lastname = lastname.capitalize()
                if initials:
                    initials = ' '.join(i + '.' for i in parse_initial(initials))
                    authors.append(', '.join((lastname, initials)))
                    continue
                authors.append(lastname)

    # Parse group_author field
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

    # Parse year in date if no 'year' input
    if year is None:
        if date:
            try:
                parsed = parse_year(date)[0]
            except IndexError:
                pass
            else:
                if parsed[0].isdigit():
                    year = parsed[0]
                elif parsed[-1].isdigit():
                    year = parsed[-1]

    # Generates and returns date annotation (year only) in APA format
    if year is not None and year.isdigit():
        datefmt = '%Y' if len(year) == 4 else '%y'
        try:
            dp = datetime.strptime(year, datefmt)
        except ValueError:
            pass
        else:
            cur_year = datetime.now().year
            if dp.year > cur_year:
                dp = dp.replace(year=dp.year-100)
            return ' (%s).' % dp.year

    # Return empty if errors or no year found
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
            if end_page and end_page != '+':
                ret += ', %s-%s' % (begin_page, end_page)
            else:
                ret += ', %s' % begin_page
        if not ret.endswith('.'):
            ret += '.'
    return ret


def gen_doi(doi):
    """Generates DOI number in APA format using original DOI."""
    return ' doi:%s' % doi if doi else ''


def gen_location(location):
    """Generates location string in APA format from original location."""
    if location:
        location = ' Paper presented at %s' % location
        if not location.endswith('.'):
            location += '.'
        return location
    return ''


def gen_article_citation(**fields):
    """Generates article citation using article data."""

    # Authors are present
    if fields.get('author') or fields.get('group_author'):
        fmt = '{author}{date}{title}{journal}'
    # Authors are missing
    else:
        fmt = '{title}{date}{journal}'
    # Return citation
    return fmt.format(
        author=gen_author(author=fields.get('author'), group_author=fields.get('group_author')),
        date=gen_date(date=fields.get('pub_date'), year=fields.get('pub_year')),
        title=gen_title(title=fields.get('article_title'), special_issue=fields.get('special_issue')),
        journal=gen_journal(title=fields.get('pub_name'), volume=fields.get('volume'), issue=fields.get('issue'),
                            begin_page=fields.get('begin_page'), end_page=fields.get('end_page'))
    ).strip()


def gen_conf_citation(**fields):
    """Generates conference citation using article data."""

    # Authors are present
    if fields.get('author') or fields.get('group_author'):
        fmt = '{author}{date}{title}{location}'
    # Authors are missing
    else:
        fmt = '{title}{date}{location}'
    # Return citation
    return fmt.format(
        author=gen_author(author=fields.get('author'), group_author=fields.get('group_author')),
        date=gen_date(date=fields.get('conf_date')),
        title=gen_title(title=fields.get('conf_title')),
        location=gen_location(location=fields.get('conf_location'))
    ).strip()


def gen_citations(**fields):
    """Generate all citations for a specific article based on article data."""

    ret = []
    # Article reference
    if fields.get('article_title'):
        ret.append(
            Citation(value=gen_article_citation(**fields), article_id=fields['id'])
        )
    # Conference reference
    if fields.get('conf_title'):
        ret.append(
            Citation(value=gen_conf_citation(**fields), article_id=fields['id'])
        )
    # Return all generated citations or empty if not found
    return ret


def parse_row(row):
    """Parses CSV row into Article object."""
    fields = OrderedDict(
        author=row.author.strip(),
        author_full_name=row.author_full_name.strip(),
        group_author=row.group_author.strip(),
        article_title=refine_article_title(row.article_title).strip(),
        pub_name=row.pub_name.strip(),
        pub_date=row.pub_date.strip(),
        pub_year=row.pub_year.strip(),
        volume=row.volume.strip(),
        issue=row.issue.strip(),
        special_issue=row.special_issue.strip(),
        begin_page=row.begin_page.strip(),
        end_page=row.end_page.strip(),
        conf_title=row.conf_title.strip(),
        conf_date=row.conf_date.strip(),
        conf_location=row.conf_location.strip(),
        article_number=row.article_number.strip(),
        index=int(row.index.strip()),
        doi=row.doi.strip()
    )
    return Article(**fields)


def main():
    """Main method for the tool."""

    # Read input arguments
    args = get_args()

    print('Reading file %s...' % args.file)
    rows = read_csv(file=args.file)

    if rows:
        print('Found %d rows in the file.' % len(rows))
        time.sleep(.5)

        print('Loading articles...')
        objects = [parse_row(row) for row in rows]

        if objects:
            print('Resetting database...')
            db_init_or_reset()

            print('Inserting articles into the database...')
            db.session.bulk_save_objects(objects)
            db.session.commit()
            db.session.close()
            time.sleep(.5)

            print('Generating citations for the articles...')
            articles = Article.query.all()
            objects = []
            for article in articles:
                fields = {k: v for k, v in article.__dict__.items() if not k.startswith('_')}
                objects.extend(gen_citations(**fields))

            if objects:
                print('Inserting citations into the database...')
                db.session.bulk_save_objects(objects)
                db.session.commit()
                db.session.close()
                time.sleep(.5)
            else:
                print('No citation was generated.')

            print('Done.')
            return

        else:
            print('No article found.')

    else:
        print('No row in file.')


if __name__ == '__main__':
    main()
