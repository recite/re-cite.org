# -*- coding: ascii -*-
"""
app.views
~~~~~~~~~

Rendering application pages.
"""

from flask import render_template, request, flash
from . import app
from .models import Article, Citation
from .utils import parse_citations, matching, doi_normalize


def highlight_matches(text):
    """
    Parse input text into a list of citations, highlight matched citations

    :param text:    input text
    :type text:     str
    :return:        highlighted text (or original text if not found)
    :rtype:         str
    """

    # Parse input text into list of citations
    found = parse_citations(text)

    # Citations found
    if found:

        # Load all available citations from local DB used for matching
        articles = Article.query.all()
        dois = set(doi_normalize(a.doi) for a in articles if a.doi)
        citations = Citation.query.all()

        # Do matching for each citation found
        for citation in found:
            matched = matching(citation, dois, citations, max_distance=app.config['MAX_EDIT_DISTANCE'])
            if matched.endswith('</mark>'):
                text = text.replace(citation, matched)

        # Return highlighted text which matched citations
        return text

    # Return nothing if no citation found
    return None


def handle_post(data, **kwargs):
    """
    Process posted citations as POST data

    :param data:    posted citations as POST data
    :type data:     str
    :param kwargs:  arbitrary key-value pairs used for page rendering
    :return:        rendered Index page with text highlighted
    """

    # Find and highlight matches in data
    highlights = highlight_matches(text=data)

    # No highlights or matches found
    if highlights is None:
        flash('No citations found. Likely reason: citations were not in the correct format.', 'failed')
        highlights = data

    # Highlights found
    elif '</mark>' not in highlights:
        flash('No citations matched retracted articles in our database.')

    # Return rendered Index page with highlights and original text
    return render_template('index.html', highlights=highlights, text=data, **kwargs)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main index page of application. Accepts both GET and POST methods"""

    kwargs = {
        'title': app.config['INDEX_PAGE_TITLE'],
        'header': app.config['INDEX_PAGE_HEADER']
    }

    # Method is POST
    if request.method == 'POST':
        data = request.form.get('citations')
        if data:
            return handle_post(data, **kwargs)

    # Method is GET or POST with empty data
    return render_template('index.html', **kwargs)


@app.route('/about')
def about():
    """Renders About page"""

    kwargs = {
        'title': app.config['ABOUT_PAGE_TITLE'],
        'header': app.config['ABOUT_PAGE_HEADER']
    }
    return render_template('about.html', **kwargs)


@app.route('/contact')
def contact():
    """Renders Contact page"""

    kwargs = {
        'title': app.config['CONTACT_PAGE_TITLE'],
        'header': app.config['CONTACT_PAGE_HEADER']
    }
    return render_template('contact.html', **kwargs)


@app.route('/how_to')
def how_to():
    """Renders About page"""

    kwargs = {
        'title': app.config['HOWTO_PAGE_TITLE'],
        'header': app.config['HOWTO_PAGE_HEADER']
    }
    return render_template('how_to.html', **kwargs)
