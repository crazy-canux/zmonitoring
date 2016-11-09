# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__all__ = [
    # Engine
    'engine',
    'session',
    # Tables
    'Projects',
    'Issues',
    'IssueStatus',
    'Journals',
    'JournalDetails',
    # Queries
    'issues',
    'versions',
]

from django.conf import settings
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection



# Redmine database connection string
REDMINE_CONN_STRING = ('mysql://'
                       '{REDMINE_USER}:{REDMINE_PASSWORD}'
                       '@{REDMINE_DB_HOST}/{REDMINE_DB}')

# Database engine setup
Base = declarative_base(cls=DeferredReflection)
engine = create_engine(REDMINE_CONN_STRING.format(**settings.REDMINE_DATABASE), pool_recycle=3600, pool_size=10)

# Creating a session
DbSession = sessionmaker(bind=engine)
session = DbSession()


# Declare database tables
class IssueStatus(Base):
    __tablename__ = 'issue_statuses'


class Projects(Base):
    __tablename__ = 'projects'

    def __repr__(self):
        return "<Projects: {0.name}>".format(self)


class Journals(Base):
    __tablename__ = 'journals'

    # Related objects
    entries = relationship(
       'JournalDetails',
       primaryjoin='Journals.id==JournalDetails.journal_id',
       foreign_keys='JournalDetails.journal_id')


class JournalDetails(Base):
    __tablename__ = 'journal_details'


class CustomValues(Base):
    __tablename__ = 'custom_values'
    customized_id = Column(Integer, ForeignKey('issues.id'))


class Users(Base):
    __tablename__ = 'users'


class Versions(Base):
    __tablename__ = 'versions'

    # Foreign keys
    project_id = Column(Integer, ForeignKey('projects.id'))

    # Related objects
    project = relationship('Projects')

    def __repr__(self):
        return "<Versions: {0.project} / {0.name}>".format(self)


class Issues(Base):
    __tablename__ = 'issues'

    # Foreign keys
    status_id = Column(Integer, ForeignKey('issue_statuses.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    fixed_version_id = Column(Integer, ForeignKey('versions.id'))

    # Related objects
    user_assigned = relationship('Users',
                        primaryjoin='Users.id==Issues.assigned_to_id',
                           foreign_keys='Issues.assigned_to_id')
    user_created = relationship('Users',
                        primaryjoin='Users.id==Issues.author_id',
                           foreign_keys='Issues.author_id')
    status = relationship('IssueStatus')
    project = relationship('Projects')
    roadmap = relationship('Versions')
    journal = relationship('Journals',
                           primaryjoin='Issues.id==Journals.journalized_id',
                           foreign_keys='Journals.journalized_id',
                           order_by='Journals.created_on')
    custom_values = relationship("CustomValues")

    def __repr__(self):
        return "<Issues: {0.subject}>".format(self)


Base.prepare(engine)

# Queries
issues = session.query(Issues)
versions = session.query(Versions)
