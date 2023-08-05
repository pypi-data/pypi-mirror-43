import os
from subprocess import check_call, CalledProcessError, STDOUT, PIPE, Popen

from logilab.common.testlib import unittest_main

import cubicweb.devtools  # noqa: F401 set up sys.path
from cubicweb_vcsfile.testutils import VCSFileTC

os.environ['HGRCPATH'] = os.devnull


class HGObsBaseTC(VCSFileTC):
    @classmethod
    def _create_repo(cls, cnx):
        return cnx.create_entity(
            'Repository', type=cls.repo_type, local_cache=cls.repo_path,
            encoding=cls.repo_encoding,
            title=cls.repo_title)


class HGPhasesTC(HGObsBaseTC):
    repo_type = u'mercurial'
    _repo_path = u'hgphases'


    def read_phases(self, cnx):
            return cnx.execute('Any P ORDERBY R WHERE R from_repository REPO, '
                                'R phase P, R is Revision, REPO eid %(repo)s',
                                {'repo': self.vcsrepoeid}).rows

    def test_phases(self):
        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertEqual(self.read_phases(cnx),
                             [[u'public'], [u'draft'], [u'secret']])
            self.assertEqual(vcsrepo.branch_head().phase, u'secret')
            self.assertEqual(vcsrepo.branch_head(public_only=True).phase, u'public')
            rpath = self.repo_path
            check_call(['hg', 'phase', '-R', rpath, '-p', 'all()'])
        self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertEqual(self.read_phases(cnx),
                             [[u'public'], [u'public'], [u'public']])
            self.assertEqual(vcsrepo.branch_head().eid,
                             vcsrepo.branch_head(public_only=True).eid)
            check_call(['hg', 'phase', '-R', rpath, '-fs', 'all()'])
            check_call(['hg', 'phase', '-R', rpath, '-d', '0'])
        self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            self.assertEqual(self.read_phases(cnx),
                             [[u'draft'], ['secret'], [u'secret']])
            self.assertEqual(vcsrepo.branch_head().phase, u'secret')
            self.assertIsNone(vcsrepo.branch_head(public_only=True))

    def test_author(self):
        # don't crash if the author field is longer than we like
        author = 'x' * 100 + '@' + 'y' * 100
        rpath = self.repo_path
        fpath = os.path.join(rpath, 'foo')
        with open(fpath, 'wb') as foo:
            foo.write(b'Hello, World!')
        check_call(['hg', 'commit', '-R', rpath, '-m', 'long author', '-u', author])
        self.refresh()


class HGObsRepoTC(HGObsBaseTC):
    repo_type = u'mercurial'
    _repo_path = u'hgobsolete'

    def get_id(self, rpath, rev):
        '''returns the full hex node of a revision'''
        cmd = ['hg', '-R', rpath, 'id', '--debug', '--id', '--rev', str(rev)]
        child = Popen(cmd, stdout=PIPE)
        rid, _ = child.communicate()
        rid = rid.strip()
        assert len(rid) == 40, rid
        return rid

    def test_obsolescence(self):
        # "ctx.description", ctx.rev, [(desc, rev) for p in precs]
        # reverse revision order
        ### Step 1: initial import
        
        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            expected = frozenset([
                        (u'4c1c7b25988b', u'a new foo', frozenset([
                            (u'be87eb6c1dd2', u'merge'),
                            (u'ca3bcdbaa99c', u'a new foo'),
                            (u'3eb4a1f19dda', u'amends 57625ed710010d9a357934f4bd5a0965da00a89e'),
                            (u'57625ed71001', u'a new foo'),
                            (u'2a39ec776827', u'a new foo')])),
                        (u'be87eb6c1dd2', u'merge', frozenset()),
                        (u'ca3bcdbaa99c', u'a new foo', frozenset([(u'57625ed71001', u'a new foo')])),
                        (u'2a39ec776827', u'a new foo', frozenset([
                            (u'3eb4a1f19dda', u'amends 57625ed710010d9a357934f4bd5a0965da00a89e'),
                            (u'57625ed71001', u'a new foo')])),
                        (u'3eb4a1f19dda', u'amends 57625ed710010d9a357934f4bd5a0965da00a89e', frozenset()),
                        (u'57625ed71001', u'a new foo', frozenset()),
                        (u'0361811034f0', u'base', frozenset())])
            got = frozenset([(r.changeset, r.description,
                              frozenset([(p.changeset, p.description)
                                         for p in r.obsoletes]))
                             for r in vcsrepo.reverse_from_repository
                             if r.__regid__ == 'Revision'])
            self.assertEqual(expected, got)

        ### Step 2: New commit + new amend
        rpath = self.repo_path
        with open(os.path.join(rpath, 'foo'), 'a') as foo:
            foo.write('Argh.')
        check_call(['hg', 'ci', '-R', rpath, '-m', 'ok go'])
        with open(os.path.join(rpath, 'foo'), 'w') as foo:
            foo.write('Hello, World.')
        check_call(['hg', 'commit', '--amend', '-R', rpath, '-m', 'ok go'])
        revs = self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            expected = frozenset([
                (revs[0], u'base', frozenset([])),
                (revs[1], u'a new ', frozenset([])),
                (revs[2], u'amends', frozenset([])),
                (revs[3], u'a new ', frozenset([(revs[2], u'amends'),
                                                (revs[1], u'a new ')])),
                (revs[4], u'a new ', frozenset([(revs[1], u'a new ')])),
                (revs[5], u'merge', frozenset([])),
                (revs[6], u'a new ', frozenset([(revs[5], u'merge'),
                                                (revs[4], u'a new '),
                                                (revs[3], u'a new '),
                                                (revs[2], u'amends'),
                                                (revs[1], u'a new ')])),
                (revs[7], u'ok go', frozenset([])),
                (revs[8], u'tempor', frozenset([])),
                (revs[9], u'ok go', frozenset([(revs[7], u'ok go')]))
            ])
            got = frozenset([(r.changeset,
                              r.description[:6],
                              frozenset([(p.changeset, p.description[:6],) for p in r.obsoletes]))
                             for r in vcsrepo.reverse_from_repository
                             if r.__regid__ == 'Revision'])
            self.assertEqual(expected, got)

        ### Step 3: change phrase of 6 and 9
        check_call(['hg', 'phase', '-p', '6', '9', '-R', rpath])
        self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            expected = frozenset([
                (revs[0], u'public', False, frozenset([])),
                (revs[1], u'draft', True, frozenset()),
                (revs[2], u'draft', True, frozenset()),
                (revs[3], u'draft', True, frozenset([(revs[2], u'amends', True), (revs[1], u'a new ', True)])),
                (revs[4], u'draft', True, frozenset([(revs[1], u'a new ', True)])),
                (revs[5], u'draft', True, frozenset()),
                (revs[6], u'public', False, frozenset([(revs[5], u'merge', True),
                                                       (revs[4], u'a new ', True),
                                                       (revs[3], u'a new ', True),
                                                       (revs[2], u'amends', True),
                                                       (revs[1], u'a new ', True)])),
                (revs[7], u'draft', True, frozenset()),
                (revs[8], u'draft', True, frozenset()),
                (revs[9], u'public', False, frozenset([(revs[7], u'ok go', True)]))
            ])
            got = frozenset([(r.changeset,
                              r.phase, bool(r.hidden),
                              frozenset([(p.changeset,
                                          p.description[:6],
                                          bool(p.hidden)) for p in r.obsoletes]))
                             for r in vcsrepo.reverse_from_repository
                             if r.__regid__ == 'Revision'])
            self.assertEqual(expected, got)

            # now, let's sollicitate a bit update_hidden ....
            RQL = 'Revision R WHERE R changeset %(cs)s, R hidden %(h)s'
            self.assertTrue(cnx.execute(RQL, {'cs': revs[1], 'h': True}))

        try:
            check_call(['hg', 'phase', '-p', '1', '-R', rpath, '--hidden'],
                       stdout=open(os.devnull, 'w'), stderr=STDOUT)
        except CalledProcessError:
            check_call(['hg', 'phase', '-p', '1', '-R', rpath])
        with open(os.path.join(rpath, 'foo'), 'a') as foo:
            foo.write('gunk.')
        check_call(['hg', 'ci', '-m', 'new draft', '-R', rpath])
        revs = self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            self.assertTrue(cnx.execute(RQL, {'cs': revs[1], 'h': False}))
            self.assertTrue(cnx.execute(RQL, {'cs': revs[10], 'h': False}))

        with open(os.path.join(rpath, 'foo'), 'a') as foo:
            foo.write('more gunk (hides the previous).')
        check_call(['hg', 'commit', '--amend', '-m', 'new draft', '-R', rpath])
        revs = self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            self.assertTrue(cnx.execute(RQL, {'cs': revs[1], 'h': False}))
            self.assertTrue(cnx.execute(RQL, {'cs': revs[10], 'h': True}))
            self.assertTrue(cnx.execute(RQL, {'cs': revs[11], 'h': True})) # the "amend" cset ...
            self.assertTrue(cnx.execute(RQL, {'cs': revs[12], 'h': False}))

        # obsolescence revision added betwen known changeset
        # (issue #2731056)
        # preparation:
        with open(os.path.join(rpath, 'foo'), 'a') as foo:
            foo.write('some more stuff\n')
        check_call(['hg', 'commit', '-m', 'stuff', '-R', rpath])
        revs = self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            expected = frozenset([
                (revs[0], u'public', False, frozenset([])),
                (revs[1], u'public', False, frozenset([])),
                (revs[2], u'draft', True, frozenset([])),
                (revs[3], u'draft', True, frozenset([(revs[2], u'amends', True), (revs[1], u'a new ', False)])),
                (revs[4], u'draft', True, frozenset([(revs[1], u'a new ', False)])),
                (revs[5], u'draft', True, frozenset([])),
                (revs[6], u'public', False, frozenset([(revs[5], u'merge', True),
                                                        (revs[4], u'a new ', True),
                                                        (revs[3], u'a new ', True),
                                                        (revs[2], u'amends', True),
                                                        (revs[1], u'a new ', False)])),
                (revs[7], u'draft', True, frozenset([])),
                (revs[8], u'draft', True, frozenset([])),
                (revs[9], u'public', False, frozenset([(revs[7], u'ok go', True)])),
                (revs[10], u'draft', True, frozenset([])),
                (revs[11], u'draft', True, frozenset([])),
                (revs[12], u'draft', False, frozenset([(revs[10], u'new dr', True)])),
                (revs[13], u'draft', False, frozenset([])),
            ])
            got = frozenset([(r.changeset,
                              r.phase,
                              bool(r.hidden),
                              frozenset([(p.changeset,
                                          p.description[:6],
                                          bool(p.hidden)) for p in r.obsoletes]))
                             for r in vcsrepo.reverse_from_repository
                             if r.__regid__ == 'Revision'])
            self.assertEqual(expected, got)

        # preparation: Adding an obsolescence relation
        id_succ = self.get_id(rpath, 12)
        id_prec = self.get_id(rpath, 13)
        check_call(['hg', 'debugobsolete', id_prec, id_succ, '-R', rpath])
        check_call(['hg', 'up', '12', '-R', rpath])
        revs = self.refresh()

        with self.admin_access.repo_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            expected = frozenset([
                (revs[0], u'public', False, frozenset([])),
                (revs[1], u'public', False, frozenset([])),
                (revs[2], u'draft', True, frozenset([])),
                (revs[3], u'draft', True, frozenset([(revs[2], u'amends', True), (revs[1], u'a new ', False)])),
                (revs[4], u'draft', True, frozenset([(revs[1], u'a new ', False)])),
                (revs[5], u'draft', True, frozenset([])),
                (revs[6], u'public', False, frozenset([(revs[5], u'merge', True),
                                                        (revs[4], u'a new ', True),
                                                        (revs[3], u'a new ', True),
                                                        (revs[2], u'amends', True),
                                                        (revs[1], u'a new ', False)])),
                (revs[7], u'draft', True, frozenset([])),
                (revs[8], u'draft', True, frozenset([])),
                (revs[9], u'public', False, frozenset([(revs[7], u'ok go', True)])),
                (revs[10], u'draft', True, frozenset([])),
                (revs[11], u'draft', True, frozenset([])),
                (revs[12], u'draft', False, frozenset([(revs[13], u'stuff', True),
                                                       (revs[10], u'new dr', True)])),
                (revs[13], u'draft', True, frozenset([])),
            ])
            got = frozenset([(r.changeset,
                              r.phase,
                              bool(r.hidden),
                              frozenset([(p.changeset,
                                          p.description[:6],
                                          bool(p.hidden)) for p in r.obsoletes]))
                             for r in vcsrepo.reverse_from_repository
                             if r.__regid__ == 'Revision'])
            self.assertEqual(expected, got)


if __name__ == '__main__':
    unittest_main()
