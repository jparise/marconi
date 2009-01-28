# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

import struct
from twisted.web import error, resource
from zope.interface import implements

CONTENT_TYPE = 'application/x-dmap-tagged'
ALLOWED_VERSIONS = ('1.0', '2.0')

# Content Types
#
# The following section provides definitions for a number of type classes.
# These serve two purposes: first, they form a simple "traits" system for type
# properties and introspection; and second, they provide a simple serialization 
# system for the basic types.

class Byte(int):
    """A serializable 1-byte integer."""

    id = 1
    size = 1

    def serialize(self):
        """Serialize the byte value into a 1-byte big-endian string."""
        assert(struct.calcsize('>B') == self.size)
        return struct.pack('>B', self)

class Short(int):
    """A serializable 2-byte short integer."""

    id = 3
    size = 2

    def serialize(self):
        """Serialize the short integer value into a 2-byte big-endian string."""
        assert(struct.calcsize('>h') == self.size)
        return struct.pack('>h', self)

class Int(int):
    """A serializable 4-byte integer."""

    id = 5
    size = 4

    def serialize(self):
        """Serialize the integer value into 4-byte big-endian string."""
        assert(struct.calcsize('>i') == self.size)
        return struct.pack('>i', self)

class Long(long):
    """A serializable 8-byte long integer."""

    id = 7
    size = 8

    def serialize(self):
        """Serialize the long integer value into an 8-byte big-endian string."""
        assert(struct.calcsize('>q') == 8)
        return struct.pack('>q', self)

class String(str):

    id = 9
    size = property(len)

    def serialize(self):
        return struct.pack('>s', self)

class Date(int):

    id = 10
    size = 4

    def serialize(self):
        """Serialize the date into a 4-byte big-endian string."""
        assert(struct.calcsize('>i') == self.size)
        return struct.pack('>i', self)

class Version(int):
    """A serializable 4-byte version number."""

    id = 11
    size = 4

    def serialize(self):
        """Serialize the version number into a 4-byte big-endian string."""
        assert(struct.calcsize('>i') == self.size)
        return struct.pack('>i', self)

class List(object):

    id = 12
    size = 0

    def serialize(self):
        return ''

#
# Content Codes
#

class ContentCode(object):

    __slots__ = ('type', 'name')

    def __init__(self, type, name):
        self.type = type
        self.name = name

"""Recognized Content Codes"""
_codes = {
    'mstt': ContentCode(Int,        'dmap.status'),
    'miid': ContentCode(Int,        'dmap.itemid'),
    'minm': ContentCode(String,     'dmap.itemname'),
    'mikd': ContentCode(Byte,       'dmap.itemkind'),
    'mper': ContentCode(Long,       'dmap.persistentid'),
    'mcon': ContentCode(List,       'dmap.container'),
    'mcti': ContentCode(Int,        'dmap.containeritemid'),
    'mpco': ContentCode(Int,        'dmap.parentcontainerid'),
    'msts': ContentCode(String,     'dmap.statusstring'),
    'mimc': ContentCode(Int,        'dmap.itemcount'),
    'mctc': ContentCode(Int,        'dmap.containercount'),
    'mrco': ContentCode(Int,        'dmap.returnedcount'),
    'mtco': ContentCode(Int,        'dmap.specifiedtotalcount'),
    'mlcl': ContentCode(List,       'dmap.listing'),
    'mlit': ContentCode(List,       'dmap.listingitem'),
    'mbcl': ContentCode(List,       'dmap.bag'),
    'mdcl': ContentCode(List,       'dmap.dictionary'),

    'msrv': ContentCode(List,       'dmap.serverinforesponse'),
    'msau': ContentCode(Byte,       'dmap.authenticationmethod'),
    'mslr': ContentCode(Byte,       'dmap.loginrequired'),
    'mpro': ContentCode(Version,    'dmap.protocolversion'),
    'apro': ContentCode(Version,    'protocolversion'),
    'msal': ContentCode(Byte,       'dmap.supportsuatologout'),
    'msup': ContentCode(Byte,       'dmap.supportsupdate'),
    'mspi': ContentCode(Byte,       'dmap.supportspersistentids'),
    'msex': ContentCode(Byte,       'dmap.supportsextensions'),
    'msbr': ContentCode(Byte,       'dmap.supportsbrowse'),
    'msqy': ContentCode(Byte,       'dmap.supportsquery'),
    'msix': ContentCode(Byte,       'dmap.supportsindex'),
    'msrs': ContentCode(Byte,       'dmap.supportsresolve'),
    'mstm': ContentCode(Int,        'dmap.timeoutinterval'),
    'msdc': ContentCode(Int,        'dmap.databasescount'),

    'mccr': ContentCode(List,       'dmap.contentcodesresponse'),
    'mcnm': ContentCode(Int,        'dmap.contentcodesnumber'),
    'mcna': ContentCode(String,     'dmap.contentcodesname'),
    'mcty': ContentCode(Short,      'dmap.contentcodestype'),

    'mlog': ContentCode(List,       'dmap.loginresponse'),
    'mlid': ContentCode(Int,        'dmap.sessionid'),

    'mupd': ContentCode(List,       'dmap.updateresponse'),
    'msur': ContentCode(Int,        'dmap.serverrevision'),
    'muty': ContentCode(Byte,       'dmap.updatetype'),
    'mudl': ContentCode(List,       'dmap.deletedidlisting'),

    'avdb': ContentCode(List,       'serverdatabases'),
    'abro': ContentCode(List,       'databasebrowse'),
    'abal': ContentCode(List,       'browsealbumlistung'),
    'abar': ContentCode(List,       'browseartistlisting'),
    'abcp': ContentCode(List,       'browsecomposerlisting'),
    'abgn': ContentCode(List,       'browsegenrelisting'),

    'adbs': ContentCode(List,       'databasesongs'),
    'asal': ContentCode(String,     'songalbum'),
    'asar': ContentCode(String,     'songartist'),
    'asbt': ContentCode(Short,      'songsbeatsperminute'),
    'asbr': ContentCode(Short,      'songbitrate'),
    'ascm': ContentCode(String,     'songcomment'),
    'asco': ContentCode(Byte,       'songcompilation'),
    'asda': ContentCode(Date,       'songdateadded'),
    'asdm': ContentCode(Date,       'songdatemodified'),
    'asdc': ContentCode(Short,      'songdisccount'),
    'asdn': ContentCode(Short,      'songdiscnumber'),
    'asdb': ContentCode(Byte,       'songdisabled'),
    'aseq': ContentCode(String,     'songeqpreset'),
    'asfm': ContentCode(String,     'songformat'),
    'asgn': ContentCode(String,     'songgenre'),
    'asdt': ContentCode(String,     'songdescription'),
    'asrv': ContentCode(Byte,       'songrelativevolume'),
    'assr': ContentCode(Int,        'songsamplerate'),
    'assz': ContentCode(Int,        'songsize'),
    'asst': ContentCode(Int,        'songstarttime'),
    'assp': ContentCode(Int,        'songstoptime'),
    'astm': ContentCode(Int,        'songtime'),
    'astc': ContentCode(Short,      'songtrackcount'),
    'astn': ContentCode(Short,      'songtracknumber'),
    'asur': ContentCode(Byte,       'songuserrating'),
    'asyr': ContentCode(Short,      'songyear'),
    'asdk': ContentCode(Byte,       'songdatakind'),
    'asul': ContentCode(String,     'songdataurl'),

    'aply': ContentCode(List,       'databaseplaylists'),
    'abpl': ContentCode(Byte,       'baseplaylist'),

    'apso': ContentCode(List,       'playlistsongs'),

    'prsv': ContentCode(List,       'resolve'),
    'arif': ContentCode(List,       'resolveinfo'),

    'aeNV': ContentCode(Int,        'com.apple.itunes.norm-volume'),
    'aeSP': ContentCode(Byte,       'com.apple.itunes.smart-playlist'),
}

#
# DAAP Data
#

class Block(object):
    """
    A Block represents a DAAP tag and typed value.  The tag must be one of
    the supported content codes, and the value's type must match the content
    code's defined type.
    """

    def __init__(self, tag, value):
        # Make sure that we've been given a supported tag.
        try:
            code = _codes[tag]
        except KeyError:
            raise ValueError("'%s'is not a supported tag" % tag)
        # Make sure that a compatible value type has been provided.
        if not isinstance(value, code.type):
            raise TypeError('Expected value of type %s (%s given)' %
                            (code.type, type(value)))

        self.tag = tag
        self.value = value
        self.size = value.size
        self.children = []

    def add(self, block):
        """Add the given block as a child of this block."""
        if not isinstance(block, Block):
            raise TypeError('Children must also be Block instances')
        # Add this new block as a child and update our total size.  Note that
        # we add an additional eight bytes to account for the child block's tag
        # and size fields.
        self.children.append(block)
        self.size += 8 + block.size

    def serialize(self):
        """Serialize this block into a dmap-tagged formatted string."""
        (code,) = struct.unpack('>i', self.tag)
        s = struct.pack('>ii', code, self.size)
        s += self.value.serialize()
        s += ''.join([child.serialize() for child in self.children])
        return s

    def __str__(self):
        """Return the DAAP-serialized representation of this block."""
        return self.serialize()

    def __repr__(self):
        """Return a human-readable representation of this block."""
        s  = "{'%s(%d)': %s" % (self.tag, self.size, repr(self.value))
        if len(self.children):
            s += ' ' + ', '.join([repr(child) for child in self.children])
        s += '}'
        return s


class Resource:
    """Base Abstract Resource"""

    implements(resource.IResource)

    isLeaf = False

    def putChild(self, path, child):
        from twisted.web.server import UnsupportedMethod
        raise UnsupportedMethod(getattr(self, 'allowedMethods', ()))

    def preRender(self, request):
        if request.method.upper() != 'GET':
            request.setResponseCode(http.BAD_REQUEST, 'Invalid request')
            return False

        # TODO: Respect the complete ALLOWED_VERSIONS set.
#        if request.getHeader('Client-DAAP-Version') != ['1.0']:
#            request.setResponseCode(http.BAD_REQUEST, 'Invalid request')
#            return False

        request.setHeader('Content-Type', CONTENT_TYPE)
        return True


class RootResource(Resource):

    def __init__(self):
        self.children = {
            'server-info':          ServerInfoResource,
            'content-codes':        ContentCodesResource,
            'login':                LoginResource,
            'update':               UpdateResource,
            'databases':            DatabasesResource,
        }

    def getChildWithDefault(self, name, request):
        try:
            return self.children[name]()
        except KeyError:
            return self

    def render(self, request):
        request.setResponseCode(http.BAD_REQUEST, 'Invalid request')
        return ''


class ServerInfoResource(Resource):
    
    isLeaf = True

    def render(self, request):
        if not self.preRender(request):
            return ''

        name = String('Marconi')

        # Respond with protocol versions appropriate to this request's client.
        version = request.getHeader('Client-DAAP-Version')
        if version and version == '1.0':
            mpro = Version(1 << 16)
            apro = Version(1 << 16)
        elif version and version == '2.0':
            mpro = Version(1 << 16)
            apro = Version(2 << 16)
        else:
            mpro = Version(2 << 16)
            apro = Version(3 << 16)

        r = Block('msrv', List())                   # server-info response
        r.add(Block('mstt', Int(200)))              # status
        r.add(Block('mpro', mpro))                  # DMAP protocol version
        r.add(Block('apro', apro))                  # DAAP protocol version
        r.add(Block('minm', name))                  # server name
        r.add(Block('msau', Byte(0)))               # authentication method
        r.add(Block('mstm', Int(1800)))             # timeout (seconds)
 
        # These blocks indicate that we support various features.  The
        # presence of these blocks is enough to signal our support, so the
        # value is required to be zero.
#       r.add(Block('msex', Byte(0)))               # extensions?
#       r.add(Block('msix', Byte(0)))               # indexing?
#       r.add(Block('msbr', Byte(0)))               # browsing?
#       r.add(Block('msqy', Byte(0)))               # querying?
#       r.add(Block('msup', Byte(0)))               # updating?
#       r.add(Block('mspi', Byte(0)))               # persistent IDs?
#       r.add(Block('msal', Byte(0)))               # auto-logout?
#       r.add(Block('msrs', Byte(0)))               # resolve (requires mspi)?

        r.add(Block('msdc', Int(1)))                # database count

        return r.serialize()

class ContentCodesResource(Resource):
    isLeaf = True


class LoginResource(Resource):
    isLeaf = True


class UpdateResource(Resource):
    isLeaf = True


class DatabasesResource(Resource):
    isLeaf = False

    def render(self, request):
        if not self.preRender(request):
            return ''

        name = String('Marconi')

        r = Block('avdb', List())                   # database response
        r.add(Block('mstt', Int(200)))              # status
        r.add(Block('muty', Byte(0)))               # update type (always 0)
        r.add(Block('mtco', Int(1)))                # matching record count
        r.add(Block('mrco', Int(1)))                # returned record count

        db = Block('mlit', List())                  # database record
        db.add(Block('miid', Int(1)))               # database id
        db.add(Block('mper', Long(1)))              # database persistent id
        db.add(Block('minm', name))                 # database name
        db.add(Block('mimc', Int(0)))               # database item count
        db.add(Block('mctc', Int(0)))               # database container count

        list = Block('mlcl', List())                # record listing
        list.add(db)

        r.add(list)

        return r.serialize()

    def getChild(self, path, request):
        print request
        return DatabaseItemsResource()

    def getChildWithDefault(self, name, request):
        return self.getChild(name, request)


class DatabaseItemsResource(Resource):
    isLeaf = True

    def render(self, request):
        if not self.preRender(request):
            return ''

        name = String('Test Song Name')

        r = Block('adbs', List())                   # song list
        r.add(Block('mstt', Int(200)))              # status
        r.add(Block('muty', Byte(0)))               # update type (always 0)
        r.add(Block('mtco', Int(1)))                # matching record count
        r.add(Block('mrco', Int(1)))                # returned record count

        song = Block('mlit', List())                # song entry
        song.add(Block('mikd', Byte(2)))            # item kind (2 for music)
        song.add(Block('miid', Int(1)))             # song id
        song.add(Block('minm', String('Name')))     # song name
        song.add(Block('mper', Long(1)))            # song persistent id

        song.add(Block('asal', String('Album')))    # song persistent id

        list = Block('mlcl', List())                # record listing
        list.add(song)

        r.add(list)

        return r.serialize()


class DatabaseContainersResource(Resource):
    isLeaf = True

    def render(self, request):
        if not self.preRender(request):
            return ''

        name = String('Test Song Name')

        r = Block('aply', List())                   # song list
        r.add(Block('mstt', Int(200)))              # status
        r.add(Block('muty', Byte(0)))               # update type (always 0)
        r.add(Block('mtco', Int(1)))                # matching record count
        r.add(Block('mrco', Int(1)))                # returned record count

        item = Block('mlit', List())                # song entry
        item.add(Block('miid', Int(1)))             # song id
        item.add(Block('mper', Long(1)))            # song persistent id
        item.add(Block('minm', String('Playlist'))) # song name
        item.add(Block('mimc', Int(0)))             # number of items

        list = Block('mlcl', List())                # record listing
        list.add(item)

        r.add(list)

        return r.serialize()


def getService(port=3689):
    """Return a DAAP server service instance attached to the given port."""
    from twisted.application.internet import TCPServer
    from twisted.web import server
    return TCPServer(port, server.Site(RootResource()))
