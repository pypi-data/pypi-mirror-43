# pylint: disable-msg=W0622
"""cubicweb-intranet application packaging information"""

modname = 'intranet'
distname = "cubicweb-intranet"

numversion = (1, 2, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
description = "an intranet built on the CubicWeb framework"
web = 'http://cubicweb.org/project/cubicweb-intranet'
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {'cubicweb': '>= 3.26.0',
               'cubicweb-blog': None,
               'cubicweb-book': None,
               'cubicweb-card': None,
               'cubicweb-link': None,
               'cubicweb-file': '>= 2.0.1',
               'cubicweb-folder': None,
               'cubicweb-tag': None,
               'cubicweb-comment': None,
               'cubicweb-task': None,
               'cubicweb-event': None,}
