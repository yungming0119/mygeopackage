import unittest
import os
import mygeopackage
import mygeopackage.regression

class Test_ols(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        print('Setup.')
        self.in_geojson = os.path.abspath(r'docs\notebooks\data\boston.geojson')
        self.geo = mygeopackage.Geo(self.in_geojson,request=False)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print('Tear down\n')

    def test_ols(self):
        """Test something."""
        self.assertIsInstance(mygeopackage.regression.ols(self.geo,11,[9],0),mygeopackage.regression.Regression)

if __name__ == '__main__':
    unittest.main()

