# pylint: disable-msg=W0622
"""cubicweb-vcsfile packaging information"""

modname = 'vcsfile'
distname = "cubicweb-%s" % modname

numversion = (2, 5, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"

author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname
description = "component to integrate version control systems data into the CubicWeb framework"

__depends__ = {
    'cubicweb': '>= 3.26.0',
    'cubicweb-localperms': '>= 0.1.0',
    'logilab-mtconverter': '>= 0.7.0',
    'logilab-common': '>= 0.59.0',
    'six': None,
    'python-hglib': None,
    'tzlocal': None,
    'docutils': None,
}

__recommends__ = {}

classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
]
