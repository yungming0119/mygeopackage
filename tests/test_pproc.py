import unittest
import os
import mygeopackage
import mygeopackage.pproc

class Test_pproc(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        print('Setup.')
        self.in_geojson = os.path.abspath(r'docs\notebooks\data\sample_points.geojson')
        self.geo = mygeopackage.Geo(self.in_geojson,request=False)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print('Tear down\n')

    def test_standardNormalization(self):
        """Test something."""
        self.assertIsNone(mygeopackage.pproc.standardNormalization(self.geo,15))

if __name__ == '__main__':
    unittest.main()

