# -*- coding: ascii -*-
"""Main config file of project."""

# PostgreSQL database configuration
DB_SETTINGS = {
    'host': 'localhost',
    'port': 5432,
    'dbname': '',
    'user': '',
    'passwd': ''
}

# Maximum Levenshtein edit distance used for approximate matching
MAX_EDIT_DISTANCE = 3

# Index page
INDEX_PAGE_TITLE = 'Highlight citations to retracted articles.'
INDEX_PAGE_HEADER = 're-cite.org'

# About page
ABOUT_PAGE_TITLE = 'About re-cite.org'
ABOUT_PAGE_HEADER = 'About'

# Contact page
CONTACT_PAGE_TITLE = 'Contact Us'
CONTACT_PAGE_HEADER = 'Contact Us'
