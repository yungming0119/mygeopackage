"""Data preprocessing module."""

from mygeopackage import *
from sklearn import preprocessing
import numpy as np

def standardNormalization(geo: type(Geo),field_index):
    """Standard Normalized a field in the dataset.

    Args:
        geo (class GEO): GEO class object that stored spatial data and attributes.
        field_index (int): The index of the field to be normalized.

    Raises:
        TypeError: [description]
    """
    if not isinstance(geo,Geo):
        raise TypeError
    scaler = preprocessing.StandardScaler()
    #print(geo.data[:,field_index])
    geo.data[:,field_index] = scaler.fit_transform(geo.data[:,field_index].reshape(-1,1)).flatten()