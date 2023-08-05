# pylint: disable=W0622
"""cubicweb-searchui application packaging information"""

modname = 'searchui'
distname = 'cubicweb-searchui'

numversion = (0, 4, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'

author_email = 'contact@logilab.fr'
description = 'set of ui components to ease data browsing'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.26.0',
    'cubicweb-squareui': None
}

__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
