# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker, MultiService
from zope.interface import implements

class Options(usage.Options):
    optParameters = [
        ['debug', '', False, "Enables debug output", bool],
        ['db', 'd', ':memory:', "The service database's path", str],
        ['name', 'n', 'Marconi', "The server's public name", str],
        ['port', 'p', 3689, "The server's port", int],
    ]

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'marconi'
    description = 'A network media server'
    options = Options

    def _createDatabase(self, options):
        from marconi import db
        return db.create(options['db'], options['debug'])

    def _getDaapService(self, library, options):
        from twisted.internet import reactor
        from marconi.net import bonjour, daap

        port = options['port']
        name = options['name']

        # The DAAP service hierarchy consists of both the DAAP protocol
        # service and the Bonjour service discovery protocol.  We add them
        # as sibling services under a common root.
        root = MultiService()

        # DAAP Protocol
        service = daap.getService(library, port=port)
        service.setServiceParent(root)

        # Bonjour Service Discovery Protocol
        service = bonjour.Service(reactor, "_daap._tcp", port, name)
        service.setServiceParent(root)

        return root

    def makeService(self, options):
        from marconi.base import Library

        # Create the server's database and library instances.
        db = self._createDatabase(options)
        library = Library(db, options['name'])

        # Create the root of our application's service hierarchy.
        root = MultiService()

        # DAAP Service
        service = self._getDaapService(library, options)
        service.setServiceParent(root)

        return root

# Create our public service maker instance.  Twisted's plugin infrastructure
# will use this to construct our service should it be requested.
serviceMaker = ServiceMaker()
