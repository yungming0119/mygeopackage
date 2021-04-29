#!/usr/bin/env python

"""Tests for `mygeopackage` package."""


import unittest

import os

from mygeopackage import mygeopackage


class TestMygeopackage(unittest.TestCase):
    """Tests for `mygeopackage` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        print('Setup.')
        self.in_geojson = r'docs/notebooks/data/sample_points.geojson'
        self.in_shp = r'docs/notebooks/data/sample_points_shp2.shp'


    def tearDown(self):
        """Tear down test fixtures, if any."""
        print('Tear down\n')

    def test_geojson_to_array(self):
        """Test something."""
        self.assertIsInstance(mygeopackage.Geo(self.in_geojson,request=False),mygeopackage.Geo)
    
    def test_shp_to_array(self):
        self.assertIsInstance(mygeopackage.Geo(self.in_shp,request=False,file_type='shp'),mygeopackage.Geo)

if __name__ == '__main__':
    unittest.main()
