# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

import pybonjour
from twisted.application import service
from twisted.internet.defer import Deferred
from twisted.internet.interfaces import IReadDescriptor
from twisted.python import log
from zope import interface

class ServiceDescriptor(object):

    interface.implements(IReadDescriptor)

    def __init__(self, sdref):
        self.sdref = sdref

    def doRead(self):
        pybonjour.DNSServiceProcessResult(self.sdref)

    def fileno(self):
        return self.sdref.fileno()

    def logPrefix(self):
        return "bonjour"

    def connectionLost(self, reason):
        self.sdref.close()

def broadcast(reactor, regtype, port, name=None):
    def _callback(sdref, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            d.callback((sdref, name, regtype, domain))
        else:
            d.errback(errorCode)

    d = Deferred()
    sdref = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = port,
                                         callBack = _callback)

    reactor.addReader(ServiceDescriptor(sdref))
    return d

class Service(service.Service):

    def __init__(self, reactor, regtype, port, name=None):
        self.reactor = reactor
        self.regtype = regtype
        self.port = port
        self.name = name
        self.sdref = None

    def startService(self):
        service.Service.startService(self)
        d = broadcast(self.reactor, self.regtype, self.port, self.name)
        d.addCallback(self._broadcasting)
        d.addErrback(self._failed)

    def stopService(self):
        if self.sdref:
            self.sdref.close()
            self.sdref = None
        return service.Service.stopService(self)

    def _broadcasting(self, args):
        self.sdref = args[0]
        log.msg('Broadcasting %s.%s%s' % args[1:])

    def _failed(self, errorCode):
        log.err(errorCode)
