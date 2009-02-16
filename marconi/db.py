# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

from sqlalchemy import Column, Integer, SmallInteger, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from twisted.python import log

Base = declarative_base()
Session = sessionmaker()

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    path = Column(Unicode(1024), unique=True)
    title = Column(Unicode)
    album = Column(Unicode)
    artist = Column(Unicode)
    bitrate = Column(SmallInteger)
    bpm = Column(SmallInteger)
    # comment
    # compilation
    # composer
    # date-added
    # date-modified
    # disc-count
    # disc-number
    # disabled
    # eq-preset
    # format
    # genre
    # description
    # relative-volume
    # sample-rate
    # size
    # start-time
    # stop-time
    # time (duration?)
    # track-count
    # track-number
    # user-rating
    # year
    # data-kind
    # data-url
    # norm-volume

    def __init__(self, path, title):
        self.path = path
        self.title = title

    def __repr__(self):
        return "<Song('%s', '%s')>" % (self.path, self.title)

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Playlist('%s')>" % (self.name,)

def create(path, debug=False):
    """
    Create a new SQLite database engine using the given path.  If the database
    doesn't already exist, it will be created.  The path ``:memory:`` will
    create a memory-based database.
    """
    import os.path
    from sqlalchemy import create_engine

    exists = os.path.exists(path)
    engine = create_engine('sqlite:///' + path, echo=debug)

    # If the database doesn't already exist, create it now.  Memory-based
    # database are always recreated from scratch.
    if path == ':memory:' or not exists:
        log.msg('Creating database: %s' % (path,))
        Base.metadata.create_all(engine)

    # Bind the table base's metadata to the new engine.  All of our tables
    # inherit from this base and will therefore be bound, as well.
    Base.metadata.bind = engine

    return engine
