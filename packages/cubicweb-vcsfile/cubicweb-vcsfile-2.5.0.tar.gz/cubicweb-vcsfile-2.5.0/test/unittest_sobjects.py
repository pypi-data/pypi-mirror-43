"""cubicweb-vcsfile unit tests for sobjects"""

from cubicweb.devtools.testlib import CubicWebTC  # noqa: F401 CW_CUBES_PATH
from cubicweb_vcsfile.testutils import VCSFileTC


class RevisionDiffServiceTC(VCSFileTC):

    def test(self):
        with self.admin_access.client_cnx() as cnx:
            diff = cnx.call_service('vcsfile.export-rev-diff',
                                    repo_eid=self.vcsrepoeid, rev1=0, rev2=1)
            expected = b'\n'.join([b'diff --git a/toto.txt b/toto.txt',
                                   b'--- a/toto.txt',
                                   b'+++ b/toto.txt',
                                   b'@@ -1,1 +1,2 @@',
                                   b' hop',
                                   b'+hop',
                                   b''])
            self.assertEqual(diff, expected)

    def test_error(self):
        with self.admin_access.client_cnx() as cnx:
            vcsrepo = cnx.entity_from_eid(self.vcsrepoeid)
            head = int(vcsrepo.cw_adapt_to('VCSRepo').head()[0])
            diff = cnx.call_service('vcsfile.export-rev-diff',
                                    repo_eid=self.vcsrepoeid, rev1=0,
                                    rev2=head + 1)
            self.assertIsNone(diff)


if __name__ == '__main__':
    import unittest
    unittest.main()
