# -*- coding: utf-8 -*-

import os
from os.path import join, abspath

from six import text_type

import hglib

from logilab.common.decorators import clear_cache

from cubicweb import ValidationError
from cubicweb.devtools.testlib import TestCase, CubicWebTC

from cubicweb_vcsfile.entities import remove_authinfo
from cubicweb_vcsfile.testutils import VCSFileTC


os.environ['HGRCPATH'] = os.devnull


class RemoveAuthInfoTC(TestCase):
    def test(self):
        self.assertEqual(remove_authinfo('http://www.logilab.org/src/cw'),
                         'http://www.logilab.org/src/cw')
        self.assertEqual(remove_authinfo('http://toto:1223@www.logilab.org/src/cw'),
                         'http://***@www.logilab.org/src/cw')


class BranchesTC(VCSFileTC):
    _repo_path = u'testrepohg_branches'
    repo_type = u'mercurial'

    def head(self, cnx, file, *args):
        vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
        revisions = vcsrepo.cw_adapt_to('VCSRepo').log_rset(file)
        return revisions.get_entity(0, 0)

    def initial(self, cnx, file, *args):
        vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
        revisions = vcsrepo.cw_adapt_to('VCSRepo').log_rset(file)
        return revisions.get_entity(-1, 0)

    def test_vcsrm(self):
        self.skipTest('gone for now')
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.grant_write_perm(cnx, 'managers', self.vcsrepoeid)
            vf = vcsrepo.versioned_file('', 'README')
            vf.vcs_rm()
            cnx.commit()
            clear_cache(vf, 'version_content')
            self.assertTrue(vf.deleted())
            # ensure parent_revision has been properly set
            self.assertTrue(vf.head.rev.parent_revision)

    def test_export_rev(self):
        # mercurial 2.6 changed export format, deal with both versions
        with hglib.open(self.repo_path) as client:
            hg26 = client.version >= (2, 6)
        date = '\n#      Mon Jun 08 17:10:24 2009 +0200' if hg26 else ''
        with self.admin_access.client_cnx() as cnx:
            rev = self.initial(cnx, 'README')
            self.assertMultiLineEqual(u'''# HG changeset patch
# User Sylvain Thénault <sylvain.thenault@logilab.fr>
# Date 1244473824 -7200%(date)s
# Node ID d846d99a7c3c715d436396778851db9eaebe55fc
# Parent  0000000000000000000000000000000000000000
initial revision (default)

diff --git a/README b/README
new file mode 100644
--- /dev/null
+++ b/README
@@ -0,0 +1,1 @@
+coucou
diff --git a/file.txt b/file.txt
new file mode 100644
--- /dev/null
+++ b/file.txt
@@ -0,0 +1,1 @@
+duh?
''' % {'date': date}, rev.export().decode('utf-8'))

    def test_adapter_branch_head(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            hgrepo = vcsrepo.cw_adapt_to('VCSRepo')
            self.assertIsNone(hgrepo.head(branch='nonexistent'))


class RepositoryTC(CubicWebTC):

    def test_repocachepath(self):
        with self.admin_access.client_cnx() as cnx:
            # with a source_url
            url = u'file://' + text_type(abspath(join(self.datadir, 'whatever')))
            hgrepo = cnx.create_entity('Repository',
                                       source_url=url, type=u'mercurial')
            cnx.commit()
            path = hgrepo.localcachepath
            self.assertEqual(['repo_cache', str(hgrepo.eid), 'whatever'],
                             path.split(os.sep)[-3:])

            # without a source_url
            hgrepo = cnx.create_entity('Repository',
                                       type=u'mercurial')
            cnx.commit()
            path = hgrepo.localcachepath
            self.assertEqual(['repo_cache', str(hgrepo.eid), 'repository'],
                             path.split(os.sep)[-3:])

            # without a source_url but with a title
            hgrepo = cnx.create_entity('Repository', title=u'my repo',
                                       type=u'mercurial')
            cnx.commit()
            path = hgrepo.localcachepath
            self.assertEqual(['repo_cache', str(hgrepo.eid), 'my_repo'],
                             path.split(os.sep)[-3:])

    def test_repo_dctitle(self):
        # with a source_url
        url = u'file://' + text_type(abspath(join(self.datadir, 'whatever')))
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.create_entity('Repository',
                                        source_url=url,
                                        type=u'mercurial')
            cnx.commit()
            self.assertEqual(vcsrepo.dc_title(), url)
            eid = vcsrepo.eid

        with self.new_access('anon').client_cnx() as cnx:
            vcsrepo = cnx.execute('Repository X WHERE X eid %(eid)s',
                                  {'eid': eid}).one()
            self.assertEqual(vcsrepo.dc_title(), url)

        # without a source_url set
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.create_entity('Repository',
                                        type=u'mercurial')
            cnx.commit()
            self.assertEqual(vcsrepo.dc_title(),
                             'mercurial repository #%s' % vcsrepo.eid)
            eid = vcsrepo.eid
        with self.new_access('anon').client_cnx() as cnx:
            vcsrepo = cnx.execute('Repository X WHERE X eid %(eid)s',
                                  {'eid': eid}).one()
            self.assertEqual(vcsrepo.dc_title(),
                             'mercurial repository #%s' % vcsrepo.eid)

    def test_unmodifiable_attrs(self):
        with self.admin_access.client_cnx() as cnx:
            url = u'file://' + text_type(abspath(join(self.datadir, 'whatever')))
            repo = cnx.create_entity('Repository', type=u'mercurial',
                                     source_url=url)
            cnx.commit()
            self.assertRaises(ValidationError, repo.cw_set, type=u'mercurial')

    def test_source_url_format(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertRaises(ValidationError, cnx.create_entity, 'Repository',
                              source_url=u'whatever', type=u'mercurial')


class AdapterTC(VCSFileTC):
    _repo_path = u'testrepohg_renaming'
    repo_type = u'mercurial'

    def test_file_deleted(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid).cw_adapt_to('VCSRepo')
            self.assertTrue(vcsrepo.file_deleted('toto.txt'))
            self.assertFalse(vcsrepo.file_deleted('tata.txt'))
            self.assertFalse(vcsrepo.file_deleted('toto.txt', '45e607c6f924'))
            self.assertTrue(vcsrepo.file_deleted('tata.txt', '45e607c6f924'))


if __name__ == '__main__':
    import unittest
    unittest.main()
