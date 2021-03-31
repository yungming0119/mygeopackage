"""Regression module."""
import numpy as np
from mygeopackage import *
import folium
from sklearn.linear_model import LinearRegression

class Regression:
    """Class object for storing regression results
    """
    def __init__(self):
        """Instantiate the Regression object.
        """
        self.identifier = 0
        self.dependent = []
        self.independent = []
        self.coef = []
        self.intercept = []
        self.score = []
        self.residuals = []

    def show(self,map=None):
        """Show regression results on interactive web map.

        Args:
            map (Folium map object, optional): If set to None, the function will create a new map object. If given the map object, the layer will be drawn on the map. Defaults to None.
        """
        if map == None:
            m = folium.Map(location=[self.residuals[0]['Location'][1],self.residuals[0]['Location'][0]],zoom_start=10)
        else:
            m = map
        max_value = max([self.residuals[i]['Residual'] for i in range(len(self.residuals))])
        min_value = min([self.residuals[i]['Residual'] for i in range(len(self.residuals))])
        for feature in self.residuals:

            interval = (max_value-min_value)/5
            if feature['Residual'] >= min_value and feature['Residual'] < min_value + interval:
                folium.CircleMarker((feature['Location'][1],feature['Location'][0]),radius=6,popup='Residual: '+str(feature['Residual']),fill=True,color='Purple',fill_color='Purple',fill_opacity=1).add_to(m)
            if feature['Residual'] >= min_value + interval and feature['Residual'] < min_value + 2 * interval:
                folium.CircleMarker((feature['Location'][1],feature['Location'][0]),radius=6,popup='Residual: '+str(feature['Residual']),fill=True,color='Blue',fill_color='Blue',fill_opacity=1).add_to(m)
            if feature['Residual'] >= min_value + 2 * interval and feature['Residual'] < min_value + 3 * interval:
                folium.CircleMarker((feature['Location'][1],feature['Location'][0]),radius=6,popup='Residual: '+str(feature['Residual']),fill=True,color='Yellow',fill_color='Yellow',fill_opacity=1).add_to(m)
            if feature['Residual'] >= min_value + 3 * interval and feature['Residual'] < min_value + 4 * interval:
                folium.CircleMarker((feature['Location'][1],feature['Location'][0]),radius=6,popup='Residual: '+str(feature['Residual']),fill=True,color='Orange',fill_color='Orange',fill_opacity=1).add_to(m)
            if feature['Residual'] >= min_value + 4 * interval and feature['Residual'] < max_value:
                folium.CircleMarker((feature['Location'][1],feature['Location'][0]),radius=6,popup='Residual: '+str(feature['Residual']),fill=True,color='Red',fill_color='Red',fill_opacity=1).add_to(m)
        display(m)


def ols(geo: type(Geo),dependent,independent,identifier):
    """Perform ordinary least square linear regression.

    Args:
        geo (class GEO): GEO class object that stored spatial data and attributes.
        dependent (int): The index of the column of dependent variable.
        independent (list): The list of indices of the columns of independent variables.
        identifier (int): The index of the column of id.

    Returns:
        class Regression: Return the regression results.
    """
    ols_results = Regression()
    ols_results.identifier = identifier
    ols_results.dependent = geo.attributes[dependent]
    ols_results.independent = [geo.attributes[i] for i in independent]
    reg = LinearRegression().fit(geo.data[:,independent],geo.data[:,dependent])
    ols_results.coef = reg.coef_
    ols_results.intercept = reg.intercept_
    ols_results.score = reg.score(geo.data[:,independent],geo.data[:,dependent])

    residuals = geo.data[:,dependent] - reg.predict(geo.data[:,independent])
    residuals_dict = {}
    for i in range(len(residuals)):
        residuals_dict['ID'] = geo.data[i][identifier]
        residuals_dict['Location'] = [geo.data[i][0],geo.data[i][1]]
        residuals_dict['Residual'] = residuals[i]
        ols_results.residuals.append(residuals_dict.copy())

    return ols_results
    
    