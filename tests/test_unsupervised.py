import unittest
import os
import mygeopackage
import mygeopackage.unsupervised

class Test_unsupervised(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        print('Setup.')
        self.in_geojson = os.path.abspath(r'docs\notebooks\data\sample_points.geojson')
        self.geo = mygeopackage.Geo(self.in_geojson,request=False)
        self.cluster_results = mygeopackage.unsupervised.Cluster(self.geo.data[0:100])

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print('Tear down\n')

    def test_k_means(self):
        """Test something."""
        self.assertIsNone(mygeopackage.unsupervised.k_means(10,[0,1],self.cluster_results,2))

    def test_dbscan(self):
        self.assertIsNone(mygeopackage.unsupervised.dbscan(0.5,5,[0,1],self.cluster_results,2))

if __name__ == '__main__':
    unittest.main()

