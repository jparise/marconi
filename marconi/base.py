# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

from marconi.db import Playlist, Session, Song

class Library(object):

    def __init__(self, db, name):
        self.db = db
        self.name = name

    def __repr__(self):
        return "<Library('%s', %s)>" % (self.name, self.db)

    @property
    def songs(self):
        """Return a Query object for the library's songs."""
        session = Session(bind=self.db)
        return session.query(Song)

    @property
    def playlists(self):
        """Return a Query object for the library's playlists."""
        session = Session(bind=self.db)
        return session.query(Playlist)
