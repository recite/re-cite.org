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
from argparse import ArgumentParser
from collections import namedtuple, OrderedDict
from functools import partial
from app import db
from app.models import Article, Citation
from styles import APA, AMA

# Convention of fields in CSV file
CsvRow = namedtuple('CsvRow', 'author author_full_name group_author '
                              'article_title pub_name conf_title conf_date '
                              'conf_location researcher_id orcid pub_date '
                              'pub_year volume issue special_issue begin_page '
                              'end_page article_number doi pubmed_id index')

# Function for refining value of article title field
refine_article_title = partial(re.compile(r'\s*(\(retract(ed|ion)[^()]*\))\s*$',
                                          flags=re.IGNORECASE).sub, '')

# Function for parsing list of authors from author field
parse_author = re.compile(r'([A-Za-z-]{2,})(, ?([A-Z]+))?').match

# Function for parsing initials from a name of author
parse_initial = re.compile(r'([A-Z])').findall

# Function for parsing year from date fields
parse_year = re.compile(r'([0-9]{4}|[a-zA-Z]{3}-([0-9]{2,4}))').findall

# Citation Types
APA_JNL = 'apa_journal'
APA_CNF = 'apa_conference'
AMA_JNL = 'ama_journal'
AMA_CNF = 'ama_conference'


def get_args(*params):
    """Parses and reads input arguments from command line."""

    parser = ArgumentParser(description='Refresh database by input CSV')
    parser.add_argument('file', metavar='FILE',
                        help='retracted articles file in CSV format')

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
    """Initialize database if starting a fresh.
    Cleanup if database already exists."""

    if db.engine.has_table(Article.__tablename__):
        clear_data()
    else:
        db.create_all()


def gen_citations(**fields):
    """Generate all citations for a specific article based on article data."""

    ret = []
    id_ = fields['id']

    # Generate styles
    apa = APA(**fields)
    ama = AMA(**fields)

    # Add APA Journal
    if apa.journal:
        ret.append(Citation(value=apa.journal, type=APA_JNL, article_id=id_))

    # Add APA Conference
    if apa.conference:
        ret.append(Citation(value=apa.conference, type=APA_CNF, article_id=id_))

    # Add AMA Journal
    if ama.journal:
        ret.append(Citation(value=ama.journal, type=AMA_JNL, article_id=id_))

    # Add AMA Conference
    if ama.conference:
        ret.append(Citation(value=ama.conference, type=AMA_CNF, article_id=id_))

    # Return generated citations or empty
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
                fields = {
                    k: v for k, v in article.__dict__.items()
                    if not k.startswith('_')
                }
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
