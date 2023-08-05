"""vcsfile.views module tests"""

import cubicweb.devtools # noqa set up sys.path

from cubicweb_vcsfile.testutils import VCSFileTC
from cubicweb_vcsfile.views import primary as vcsviews


class RevViewsTC(VCSFileTC):

    def test_entity(self):
        with self.admin_access.client_cnx() as cnx:
            revs = cnx.execute('Revision R')
            v0 = revs.get_entity(0, 0)
            self.assertEqual(v0.cw_adapt_to('IPrevNext').previous_entity(), None)
            self.assertEqual(v0.cw_adapt_to('IPrevNext').next_entity().eid, revs[1][0])
            v1 = revs.get_entity(1, 0)
            self.assertEqual(v1.cw_adapt_to('IPrevNext').previous_entity().eid, v0.eid)
            self.assertEqual(v1.cw_adapt_to('IPrevNext').next_entity().eid, revs[2][0])
            v6 = revs.get_entity(6, 0)
            self.assertEqual(v6.cw_adapt_to('IPrevNext').previous_entity().eid, revs[5][0])
            self.assertEqual(v6.cw_adapt_to('IPrevNext').next_entity(), None)

    def test_primary_view(self):
        with self.admin_access.web_request() as req:
            r0rset = req.execute('Revision R LIMIT 1')
            view = self.vreg['views'].select('primary', req, rset=r0rset)
            self.assertIsInstance(view, vcsviews.RevisionPrimaryView)
            view.render()  # just check no error raised


if __name__ == '__main__':
    import unittest
    unittest.main()
