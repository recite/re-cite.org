#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
Export all the articles and valid references to a CSV.

The script accepts only one argument: path to the output file. 
If the argument is missing, a file with export-current-time as filename 
is created in the same folder as the script.

For more information, try:
    ./export.py --help
"""

import os
import re
import csv
import time
from argparse import ArgumentParser
from collections import namedtuple
from app.models import Article

APP_PATH = os.path.dirname(__file__)

CsvRow = namedtuple(
    'CsvRow',
    [
        'id', 'author', 'author_full_name', 'group_author', 'article_title', 'pub_name', 'pub_date', 'pub_year',
        'volume', 'issue', 'special_issue', 'begin_page', 'end_page', 'conf_title', 'conf_date', 'conf_location',
        'article_number', 'index', 'doi', 'apa'
    ]
)


def get_args(*params):
    """Parses and returns input arguments from command line."""

    parser = ArgumentParser(description='Export retracted articles into CSV')
    parser.add_argument('file', metavar='FILE', nargs='?', help='exported destination file path')
    args = parser.parse_args(*params)

    # Check file input
    if args.file:
        if os.path.isfile(args.file):
            parser.error('Destination file is currently existed: %s' % args.file)
        elif not re.match(r'^[Cc][Ss][Vv]$', args.file[-3:]):
            parser.error('File exported must be CSV')
    else:
        args.file = gen_file_name()

    # Return arguments
    return args


def gen_file_name():
    """Generates export file name using current time."""
    return os.path.join(APP_PATH, 'export-%s.csv' % time.strftime('%Y%m%d-%H%M%S'))


def write_csv(file, rows):
    """
    Write rows to the CSV file

    :param file:    path to the output file
    :type file:     str
    :param rows:    list of rows to be written
    :type rows:     list or tuple
    """
    rows = [CsvRow._fields] + rows
    with open(file, 'w', newline='') as fp:
        writer = csv.writer(fp, delimiter=',', quotechar='"')
        writer.writerows(rows)


def main():
    """Main export program"""

    # Read input arguments
    args = get_args()

    # Read articles from database
    print('Exporting retracted articles to %s...' % args.file)
    rows = []
    articles = Article.query.order_by(Article.id).all()
    for article in articles:
        fields = {
            k: v for k, v in article.__dict__.items()
            if not k.startswith('_') and k != 'citations'
        }
        for citation in article.citations:
            rows.append(CsvRow(**fields, apa=citation.value))

    # Write to file
    write_csv(args.file, rows)
    time.sleep(.5)
    print('Done.')


if __name__ == '__main__':
    main()
