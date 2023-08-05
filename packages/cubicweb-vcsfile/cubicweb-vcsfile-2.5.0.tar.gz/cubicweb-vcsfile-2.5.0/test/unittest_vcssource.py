# -*- coding: utf-8 -*-

import os.path as osp
from datetime import datetime

from six import text_type

from pytz import utc

from cubicweb import ValidationError
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_vcsfile.testutils import setup_repos
from cubicweb_vcsfile.testutils import VCSFileTC


class HGRepoTC(VCSFileTC):
    _repo_path = u'testrepohg'
    repo_encoding = u'latin1'

    first_revision = 0
    author = 'Sylvain Thénault <sylvain.thenault@logilab.fr>'

    def test_base(self):
        with self.admin_access.client_cnx() as cnx:
            res = cnx.execute('Revision X')
            self.assertEqual(len(res), 7)

    def test_revision_parent(self):
        with self.admin_access.client_cnx() as cnx:
            res = cnx.execute('Any R,P ORDERBY R WHERE R parent_revision P?')
            self.assertEqual(len(res), 7)
            self.assertEqual(res[0][1], None)
            latestrev = res[0][0]
            for i, (rev, parent) in enumerate(res[1:]):
                self.assertEqual(parent, latestrev)
                latestrev = rev

    def test_anon_access_data(self):
        self.skipTest('no permissions yet')
        with self.new_access('anon').client_cnx() as cnx:
            res = cnx.execute('VersionContent X LIMIT 1').get_entity(0, 0)
            self.assertTrue(res.data)
            self.assertTrue(res.data.getvalue())

    def test_error_update_repo(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertRaises(ValidationError,
                              cnx.execute, 'SET X type "subversion" WHERE X is Repository')

    def test_revision_date(self):
        with self.admin_access.client_cnx() as cnx:
            rev = cnx.execute('Any MAX(X) WHERE X is Revision').one()
            self.assertEqual(rev.creation_date, datetime(2009, 5, 26, 14, 17, 27, tzinfo=utc))


class HGRepoCreationTC(CubicWebTC):

    def test_create(self):
        with self.admin_access.client_cnx() as cnx:
            url = u'file:///path/to/nowhere'
            vcsrepo = cnx.create_entity('Repository',
                                        source_url=url, type=u'mercurial')
            cnx.commit()
            cachedir = vcsrepo.localcachepath
            self.assertTrue(osp.isabs(cachedir))
            self.assertTrue(osp.isdir(cachedir))
            # check the local cache repository has been inititalized
            # properly, but as it could not pull from source_url, it's
            # empty
            self.assertEqual(0, len(vcsrepo.cw_adapt_to('VCSRepo').log_rset()))

            # same thing without any source_url
            vcsrepo = cnx.create_entity('Repository', type=u'mercurial')
            cnx.commit()
            cachedir = vcsrepo.localcachepath
            self.assertTrue(osp.isabs(cachedir))
            self.assertTrue(osp.isdir(cachedir))
            # check the local cache repository has been inititalized
            # properly but is empty
            self.assertEqual(0, len(vcsrepo.cw_adapt_to('VCSRepo').log_rset()))

    def test_create_localcache(self):
        path = osp.join(self.datadir, 'testrepo')
        setup_repos(path)
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.create_entity('Repository', local_cache=text_type(path),
                                        type=u'mercurial')
            cnx.commit()
            self.assertEqual(path, vcsrepo.local_cache)
            cachedir = vcsrepo.localcachepath
            self.assertTrue(osp.isabs(cachedir))


class HGCachedRepoTC(VCSFileTC):
    _repo_path = u'testrepohg'
    repo_encoding = u'latin1'

    def test_cache_mgmt(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.find('Repository').one()

            self.assertFalse(osp.isabs(vcsrepo.local_cache))
            cachedir = vcsrepo.localcachepath
            self.assertTrue(osp.isabs(cachedir))
            self.assertTrue(osp.isdir(cachedir))
            cnx.execute('DELETE Repository R WHERE R eid %(r)s', {'r': vcsrepo.eid})
            cnx.commit()
            self.assertFalse(osp.isdir(cachedir))


if __name__ == '__main__':
    import unittest
    unittest.main()
