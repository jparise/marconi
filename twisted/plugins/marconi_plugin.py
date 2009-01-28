# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker, MultiService
from zope.interface import implements

class Options(usage.Options):
    optParameters = [
        ['name', 'n', 'Marconi', "The server's public name", str],
    ]

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'marconi'
    description = 'A network media server'
    options = Options

    def _getDaapService(self, options):
        from twisted.internet import reactor
        from marconi.net import bonjour, daap

        # The DAAP service hierarchy consists of both the DAAP protocol
        # service and the Bonjour service discovery protocol.  We add them
        # as sibling services under a common root.
        root = MultiService()

        # DAAP Protocol
        service = daap.getService()
        service.setServiceParent(root)

        # Bonjour Service Discovery Protocol
        service = bonjour.Service(reactor, "_daap._tcp", 3689, options['name'])
        service.setServiceParent(root)

        return root

    def makeService(self, options):
        # Create the root of our application's service hierarchy.
        root = MultiService()

        # DAAP Service
        service = self._getDaapService(options)
        service.setServiceParent(root)

        return root

# Create our public service maker instance.  Twisted's plugin infrastructure
# will use this to construct our service should it be requested.
serviceMaker = ServiceMaker()
