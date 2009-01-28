# Marconi Media Server
# Copyright 2009 Jon Parise <jon@indelible.org>

from distutils.core import setup

# Dynamically calculate the version based on marconi.VERSION.
version_tuple = __import__('marconi').VERSION
if version_tuple[2] is not None:
    version = '%d.%d_%s' % version_tuple
else:
    version = '%d.%d' % version_tuple[:2]

setup(
    name = 'marconi',
    version = version,
    description = 'Marconi Network Media Server',
    author = 'Jon Parise',
    author_email = 'jon@indelible.org',
    url = 'http://www.indelible.org/projects/marconi/',
    packages = ['marconi', 'marconi.net', 'twisted.plugins'],
    classifiers = ['Development Status :: 2 - Pre-Alpha',
                   'Environment :: No Input/Output (Daemon)',
                   'Framework :: Twisted',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Sound/Audio',
                   ],
)
