"""Unsupervised machine learning module."""

from mygeopackage import *
from mygeopackage.utility import rgb_to_hex
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import folium
import json
from random import randint
from IPython.display import display

class Cluster:   
    def __init__(self,data):
        """Instantiate the Cluster class object.

        Args:
            data (array): Numpy array containing geospatial and attribute data.
        """
        self.cluster_centers = []
        self.labels = []
        self.data = data
        self.identifier = 0
    
    def show(self,map = None, to_display=True):
        """Draw the object on the map with Folium.

        Args:
            map (Folium map object, optional): If set to None, the function will create a new map object. If given the map object, the layer will be drawn on the map. Defaults to None.
        """
        cluster_class = np.unique(self.labels)
        data = self.data
        if map == None:
            m = folium.Map(location=[data[0][1],data[0][0]],zoom_start=10)
        else:
            m = map
        for label in cluster_class:
            color = rgb_to_hex([randint(100, 255), randint(100, 255), randint(100, 255)])
            for member in self.data[np.where(self.labels == label)]:
                folium.CircleMarker([member[1],member[0]],radius=6,popup='Cluster: '+str(label),fill=True,color=color,fill_color=color,fill_opacity=1).add_to(m)
        
        if to_display == True:
            display(m)

    def toGeoJson(self):
        """Convert cluster results to Geojson

        Returns:
            GeoJSON (str): Serialized JSON text.
        """
        geojson = dict()
        geojson['type'] = 'FeatureCollection'
        geojson['name'] = 'K-Means Results'
        geojson['features'] = []

        for i in range(len(self.data)):
            item = dict()
            item['type'] = 'Feature'
            item['properties'] = dict()
            item['properties']['ID'] = self.data[i][self.identifier]
            item['properties']['Class'] = int(self.labels[i])
            item['geometry'] = dict()
            item['geometry']['type'] = 'Point'
            item['geometry']['coordinates'] = [self.data[i][0],self.data[i][1]]
            geojson['features'].append(item)
        #print(geojson)
        return json.dumps(geojson)
        

def k_means(n,field,cluster:Cluster,identifier):
    """K-Means unsupervised learning for geospatial or attribute data.

    Args:
        n (int): Desired number of clusters for K-Means analysis.
        field (int): The index for the fields to be clustered.
        cluster (Cluster): Cluster class object to store the results.
        identifier (int): The index for the field as the identifier of the dataset.
    """
    kmeans = KMeans(n_clusters=n).fit(cluster.data[:,field])
    cluster_results = cluster
    cluster_results.cluster_centers = kmeans.cluster_centers_
    cluster_results.labels = kmeans.labels_
    cluster_results.identifier = identifier
    #cluster_results = new Cluster(geo.data,kmeans.cluster_centers_,kmeans.labels_)

def dbscan(eps,min_samples,field,cluster:Cluster,identifier):
    """DBSCAN unsupervised learning for geospatial or attribute data.

    Args:
        eps (float): The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        min_samples (int): The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself.
        field (int): The index for the fields to be clustered.
        cluster (Cluster): Cluster class object to store the results.
        identifier (int): The index for the field as the identifier of the dataset.
    """
    _dbscan = DBSCAN(eps=eps,min_samples=min_samples).fit(cluster.data[:,field].astype(np.float64))
    cluster_results = cluster
    cluster_results.cluster_centers = None
    cluster_results.labels = _dbscan.labels_
    cluster_results.identifier = identifier