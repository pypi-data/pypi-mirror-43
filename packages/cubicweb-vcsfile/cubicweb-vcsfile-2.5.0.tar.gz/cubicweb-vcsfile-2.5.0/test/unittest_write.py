# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
import tempfile
from contextlib import contextmanager
from shutil import rmtree
from os import system
from os.path import join, exists
from io import BytesIO

from six import text_type

import hglib

from logilab.common.decorators import classproperty

from cubicweb import QueryError, ValidationError, Unauthorized
from cubicweb.predicates import is_instance
from cubicweb.server import hook
from cubicweb import devtools # noqa set up sys.path

from cubicweb_vcsfile import bridge
from cubicweb_vcsfile.testutils import VCSFileTC, HGRCMixin


@contextmanager
def temporary_level(level, logger=None):
    logger = logging.getLogger(logger)
    prev_level = logger.level
    logger.setLevel(level)
    yield
    logger.setLevel(prev_level)


class VCSFileWriteTCMixin(HGRCMixin):

    @classproperty
    def test_db_id(cls):
        try:
            return cls.orig_repo_path + '-write'
        except AttributeError:  # during py.test introspection
            return None

    def clear_fs_repo(self):
        # .repo_path is an absolute path
        # (pathjoin done automatically from ._repo_path)
        destpath = str(self.repo_path)
        if exists(destpath):
            rmtree(destpath)

    @classmethod
    def pre_setup_database(cls, cnx, config):
        # don't use super, _WriteTC deleted to avoid unittest2 to try to run
        # it...
        super(VCSFileWriteTCMixin, cls).pre_setup_database(cnx, config)
        cls.grant_write_perm(cnx, u'managers')

    def setUp(self):
        self.clear_fs_repo()
        super(VCSFileWriteTCMixin, self).setUp()

    def tearDown(self):
        if exists(self.vcsrepopath):
            rmtree(str(self.vcsrepopath))
        if exists(str(self.repo_path)):
            rmtree(str(self.repo_path))
        super(VCSFileWriteTCMixin, self).tearDown()

    def _test_new_revision(self, rev):
        rev.cw_clear_all_caches()
        self.assertEqual(rev.description, u'add hôp')
        self.assertEqual(rev.author, 'syt')
        self.assertEqual(rev.repository.cw_adapt_to('VCSRepo').cat(
            rev.changeset, 'toto.txt'), b'hop\nhop\nhop\n')
        self.assertTrue(rev.changeset)
        self.assertTrue(rev.parent_revision)

    def _new_toto_revision(self, cnx, data=b'hop\nhop\nhop\n', branch=None):
        newfile = ('toto.txt', BytesIO(data))
        vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
        rev = vcsrepo.make_revision(msg=u'add hôp'.encode('utf-8'),
                                    author=u'syt',
                                    branch=branch,
                                    added=[newfile], parentrev='tip')
        self.assertEqual(list(rev.created_by), [cnx.user])
        cnx.commit()
        return rev

    def import_content(self):
        with self.repo.internal_cnx() as cnx:
            bridge.import_content(cnx)
            cnx.commit()
        rpath = self.vcsrepopath
        with hglib.open(rpath) as repo:
            return dict((int(rev.rev), rev.node[:12].decode('ascii'))
                        for rev in repo.log(hidden=True))


class HGSourceWriteTC(VCSFileWriteTCMixin, VCSFileTC):
    orig_repo_path = 'testrepohg'
    _repo_path = u'newrepo'

    repo_type = u'mercurial'
    repo_encoding = u'latin1'
    repo_rev_offset = -1

    def test_new_revision_security(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.execute('DELETE CWPermission X')
            cnx.commit()
            self.assertRaises(Unauthorized, self._new_toto_revision, cnx)

    def test_rollback_new_revision(self):
        with self.admin_access.client_cnx() as cnx:
            self.skipTest('need to think some more about rollback')
            rev = self._new_toto_revision(cnx)
            cnx.rollback()
            # fail due to a bug in pysqlite, see
            # http://oss.itsystementwicklung.de/trac/pysqlite/ticket/219
            # http://www.sqlite.org/cvstrac/tktview?tn=2765,3
            # http://www.initd.org/pub/software/pysqlite/doc/usage-guide.html#controlling-transactions
            # rset = self.execute('Any X WHERE X eid %(x)s', {'x': rev.eid})
            # self.assertFalse(rset)
            rset = cnx.execute('Any X WHERE X eid %(x)s', {'x': vc.eid})
            self.assertFalse(rset)
            rset = cnx.execute('VersionContent X WHERE X content_for VF, VF eid %(vf)s',
                               {'vf': vf.eid})
            self.assertEqual(len(rset), 2)
            # XXX check actually not in the repository

    def test_validation_error_while_importing_new_revision(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertIsNone(vcsrepo.branch_head())
            hgrepo = vcsrepo.cw_adapt_to('VCSRepo')
            self.assertIsNone(hgrepo.head())

            class SytShouldntCommit(hook.Hook):
                __regid__ = 'test.addrevision'
                __select__ = hook.Hook.__select__ & is_instance('Revision')
                events = ('after_add_entity',)

                def __call__(self):
                    if self.entity.author == 'syt':
                        raise ValidationError(self.entity.eid,
                                              {'author': "please don't let syt commit"})

            with temporary_level(logging.CRITICAL + 10, 'cubicweb.appobject'):
                with self.temporary_appobjects(SytShouldntCommit):
                    with self.assertRaises(ValidationError) as cm:
                        self._new_toto_revision(cnx)
            self.assertEqual(cm.exception.errors, {'author': "please don't let syt commit"})

            vcsrepo.cw_clear_all_caches()
            self.assertIsNone(vcsrepo.branch_head())
            self.assertIsNone(hgrepo.head())

    def test_multiple_changes_and_deletion(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            added = (('toto.txt', BytesIO(b'hop\nhop\nhop\n')),
                     ('dir1/tutuu.txt', BytesIO(u'zoubî'.encode('utf-8'))))
            rev = vcsrepo.make_revision(msg=u'add hop', author=u'syt',
                                        added=added, parentrev='tip')
            self.assertEqual(rev.description, 'add hop')
            self.assertEqual(rev.author, 'syt')
            self.assertEqual(vcsrepo.cw_adapt_to('VCSRepo').cat(rev.changeset, 'toto.txt'),
                             b'hop\nhop\nhop\n')
            self.assertEqual(vcsrepo.cw_adapt_to('VCSRepo').cat(rev.changeset, 'dir1/tutuu.txt'),
                             u'zoubî'.encode('utf-8'))

        # deletion
        tmpdir = tempfile.mkdtemp()
        try:
            self.checkout(tmpdir)
            self.assertTrue(exists(join(tmpdir, 'dir1', 'tutuu.txt')))
            self.assertTrue(exists(join(tmpdir, 'toto.txt')))
        finally:
            rmtree(tmpdir)

        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            rev = vcsrepo.make_revision(msg=u'kill file', author=u'auc',
                                        deleted=('toto.txt',), parentrev='tip')

            tmpdir = tempfile.mkdtemp()
            try:
                self.checkout(tmpdir)
                self.assertTrue(exists(join(tmpdir, 'dir1', 'tutuu.txt')))
                self.assertFalse(exists(join(tmpdir, 'toto.txt')))
                self.assertFalse(exists(join(tmpdir, 'dir1', 'subdir')))
            finally:
                rmtree(tmpdir)

    def test_new_revision(self):
        with self.admin_access.client_cnx() as cnx:
            # necessary to ensure parent revision in not empty in
            # _test_new_revision
            self._new_toto_revision(cnx, data=b'initial content')
            for index, phase in enumerate(('public', 'draft', 'secret')):
                rev = self._new_toto_revision(cnx)
                cnx.commit()

                # necessary to avoid empty changeset next time
                self._new_toto_revision(cnx, data=b'modify_content')
                cnx.commit()

                # manually change phase of the latest commits
                hgrepo = hglib.open(self.vcsrepopath)
                if phase != hgrepo[rev.changeset].phase():
                    kwargs = {phase: True}
                    hgrepo.phase(revs=rev.changeset.encode('ascii'), force=True, **kwargs)
                self.import_content()
                self._test_new_revision(rev)
                self.assertEqual(rev.phase, text_type(phase))

    def checkout(self, tmpdir):
        hgcmd = 'hg clone %s %s >/dev/null 2>&1' % (self.vcsrepopath,
                                                    join(tmpdir, self.orig_repo_path))
        if system(hgcmd):
            raise Exception('can not check out %s' % self.repo_path)
        system('mv %s %s' % (join(tmpdir, self.orig_repo_path, '*'), tmpdir))
        system('mv %s %s' % (join(tmpdir, self.orig_repo_path, '.hg'), tmpdir))

    def test_branches_from_app(self):
        with self.admin_access.client_cnx() as cnx:
            self._new_toto_revision(cnx)  # add at least one rev on default
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            tip = vcsrepo.cw_adapt_to('VCSRepo').log_rset(revrange='tip').get_entity(0, 0).changeset

            # create a new branch
            rev = self._new_toto_revision(cnx, data=b'branch 1.2.3 content',
                                          branch=u'1.2.3')
            cnx.commit()
            self.assertEqual(b'hop\nhop\nhop\n',
                             vcsrepo.cw_adapt_to('VCSRepo').cat(tip, 'toto.txt'))
            self.assertEqual(b'branch 1.2.3 content',
                             vcsrepo.cw_adapt_to('VCSRepo').cat('1.2.3', 'toto.txt'))

            # create new changeset in the default branch
            rev = self._new_toto_revision(cnx, data=b'branch default content',
                                          branch='default')
            cnx.commit()
            self.assertEqual(b'branch default content',
                             vcsrepo.cw_adapt_to('VCSRepo').cat('default', 'toto.txt'))

            # create new changeset in the 1.2.3 branch
            rev = self._new_toto_revision(cnx, data=b'branch 1.2.3 new content',
                                          branch=u'1.2.3')
            cnx.commit()
            self.assertEqual(b'branch 1.2.3 new content',
                             vcsrepo.cw_adapt_to('VCSRepo').cat('1.2.3', 'toto.txt'))

            # delete toto.txt on branch default
            rev = rev.repository.make_revision(msg='delete toto.txt', author=u'titi',
                                               parentrev=u'default',
                                               deleted=('toto.txt',))
            self.assertIn(
                b'toto.txt',
                [elt[-1] for elt in vcsrepo.cw_adapt_to('VCSRepo').manifest('1.2.3')])
            self.assertNotIn(
                b'toto.txt',
                [elt[-1] for elt in vcsrepo.cw_adapt_to('VCSRepo').manifest('default')])
            cnx.commit()
            # delete toto.txt on branch 1.2.3
            rev = rev.repository.make_revision(msg='delete toto.txt in 1.2.3',
                                               author=u'toto',
                                               parentrev=u'1.2.3',
                                               deleted=('toto.txt',))
            self.assertNotIn(b'toto.txt', vcsrepo.cw_adapt_to('VCSRepo').manifest('1.2.3'))
            self.assertNotIn(b'toto.txt', vcsrepo.cw_adapt_to('VCSRepo').manifest('default'))

            # check an error occur if trying to delete an already deleted file
            with self.assertRaises(QueryError) as cm:
                rev.repository.make_revision(
                    msg='delete toto.txt in 1.2.3',
                    author=u'toto', branch=u'1.2.3', parentrev=u'1.2.3',
                    deleted=('toto.txt',))
            self.assertEqual(str(cm.exception), 'toto.txt is already deleted from the vcs')

    def test_strip_garbage_collect_vf(self):
        with self.admin_access.client_cnx() as cnx:
            for i in range(7):
                self._new_toto_revision(cnx, data=('revision %s' % i).encode('ascii'))
            cnx.commit()
        revs = self.import_content()
        self.assertEqual(7, len(revs))

        self.runindir('hg up 6 >/dev/null 2>&1')
        self.runindir('echo "new file" >> newfile.txt')
        self.runindir('hg add newfile.txt')
        self.runindir('hg ci -m "add stuff in toto"')
        revs = self.import_content()
        self.assertEqual(8, len(revs))
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertEqual(vcsrepo.latest_known_revision(), revs[7])
            self.assertIn(b'newfile.txt', vcsrepo.cw_adapt_to('VCSRepo'))

        self.runindir('hg --config extensions.hgext.mq= strip 6 1>/dev/null 2>/dev/null')
        self.import_content()
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertNotIn(b'newfile.txt', vcsrepo.cw_adapt_to('VCSRepo'))

    def test_branches_from_hg(self):
        with self.admin_access.client_cnx() as cnx:
            for i in range(7):
                self._new_toto_revision(cnx, data=('revision %s' % i).encode('ascii'))
            self.assertEqual(cnx.execute('Any COUNT(R) WHERE R is Revision').rows, [[7]])
        self.runindir('hg up default >/dev/null 2>&1')
        self.runindir('hg branch newbranch >/dev/null 2>&1')
        self.runindir('hg tag newbranch -m "opening newbranch"')
        self.import_content()

        with self.admin_access.client_cnx() as cnx:
            self.assertEqual(cnx.execute('Any COUNT(R) WHERE R is Revision').rows, [[8]])

    def runindir(self, cmd, dir=None):
        if dir is None:
            dir = self.vcsrepopath
        system('cd %s; %s' % (dir, cmd))


if __name__ == '__main__':
    import unittest
    unittest.main()
