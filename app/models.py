# -*- coding: ascii -*-
"""
app.models
~~~~~~~~~~

Contains all the model objects and their schemas.
"""

from . import db

__all__ = ['Article', 'Citation']


class Article(db.Model):
    """An article object with its table and columns defined in database"""

    #: table name in database
    __tablename__ = 'retracted_articles'
    #: ID for each article row, primary key, auto-increased
    id = db.Column(db.Integer, primary_key=True)
    #: author names of the article, required
    author = db.Column(db.Text, nullable=False)
    #: author full names, required
    author_full_name = db.Column(db.Text, nullable=False)
    #: author names if they are groups or organizations, optional
    group_author = db.Column(db.Text)
    #: title of the article, required
    article_title = db.Column(db.Text, nullable=False)
    #: publication (journal or periodical) name of article, optional
    pub_name = db.Column(db.String)
    #: date published, optional
    pub_date = db.Column(db.String)
    #: year published, optional
    pub_year = db.Column(db.String(4))
    #: volume number of a periodical where an article was published, optional
    volume = db.Column(db.String)
    #: issue number of a specific volume, optional
    issue = db.Column(db.String)
    #: special issue number, optional
    special_issue = db.Column(db.String)
    #: begin page in article where it is cited, optional
    begin_page = db.Column(db.String)
    #: end page in article where it is cited, optional
    end_page = db.Column(db.String)
    #: title if article is also a conference, optional
    conf_title = db.Column(db.Text)
    #: date when a conference was conducted, optional
    conf_date = db.Column(db.String)
    #: location where a conference was conducted, optional
    conf_location = db.Column(db.String)
    #: article number, reserved and optional
    article_number = db.Column(db.String)
    #: index number, reserved and optional
    index = db.Column(db.Integer)
    #: DOI value, optional
    doi = db.Column(db.String)
    #: list of citations generated for this article, referred to 'citations' table
    citations = db.relationship('Citation', backref='article', lazy=True)

    def __repr__(self):
        return '<Article %r>' % self.article_title


class Citation(db.Model):
    """A citation object with its table and columns defined in the database"""

    #: table name in database
    __tablename__ = 'citations'
    #: ID, primary key, auto-increased
    id = db.Column(db.Integer, primary_key=True)
    #: value of citation as unicode string, required
    value = db.Column(db.Text, nullable=False)
    #: a reference to the article to which the citation belongs to
    article_id = db.Column(db.Integer, db.ForeignKey('retracted_articles.id'), nullable=False)

    def __repr__(self):
        return '<Citation value=%r, article_id=%r>' % (self.value, self.article_id)
