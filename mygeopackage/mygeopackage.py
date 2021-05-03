"""Main module."""
import json
import os
import csv
import requests
import numpy as np
import shapefile
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, TileLayer, GeoJSON
import folium
from IPython.display import display
from .toolbar import main_toolbar
class Geo:
    uri = ""
    crs = ""
    attributes = []
    data = []

    def __init__(self,uri,request=True,x=None,y=None,header=False,output_geojson=None,file_type='geojson'):
        """Instantiate the GEO object.

        Args:
            uri (string): Local or online URI for GeoJson data.
            request (bool, optional): If set to true, the program will request the data online from the given URL, and save it in local folder. Defaults to True.
            file_type (str, optional): If the value is set to 'geojson', then the function will call GeoJsonToArray(). If the value is set to 'shp', then the function will call ShpToArray(). Defaults to 'geojson'.
            x (str, optional): Field name for X in csv.
            y (str, optional): Field name for Y in csv.
            header (bool, optional): Whether csv file contains a header. Defaults to True.
            output_geojson (str,optional): File path to output geojson for csv.
        """
        self.uri = uri
        if file_type == 'geojson':
            self.GeojsonToArray(request)
        if file_type == 'shp':
            self.ShpToArray()
        if file_type == 'csv':
            self.CsvToArray(x,y,header,output_geojson)

    def GeojsonToArray(self,request=True):
        """Convert GeoJson data to numpy array.

        Args:
            request (bool, optional): If set to true, the program will request the data online from the given URL, and save it in local folder. Defaults to True.
        """
        if os.path.exists(r'data/json_to_load.geojson') == True:
            os.remove(r'data/json_to_load.geojson')
        
        file_source = ''
        if request == True:
            response = requests.get(self.uri)
            file_source = r'data/json_to_load.geojson'
            with open(file_source,'w') as f:
                json_data = json.loads(response.text)
                json.dump(json_data,f)
        else:
            file_source = self.uri

        with open(file_source) as f:
            data = json.load(f)
            if 'crs' in data:
                crs = data['crs']['properties']['name']
                self.crs = crs
            fields = list(data['features'][0]['properties'].keys())
            arr_list = []
            for feature in data['features']:
                arr_list.append((feature['geometry']['coordinates'][0],feature['geometry']['coordinates'][1],*list(feature['properties'].values())))
            arr = np.array(arr_list)
            
            self.attributes = fields
            self.data = arr
        
    def ShpToArray(self):
        """Convert ESRI shapefile to numpy array.
        """
        if os.path.exists(self.uri):
            sf = shapefile.Reader(self.uri)
            geo_json = sf.__geo_interface__
            if os.path.exists(r'data/json_to_load_from_shp.geojson') == True:
                os.remove(r'data/json_to_load_from_shp.geojson')
            with open(r'data/json_to_load_from_shp.geojson','w') as f:                
                json.dump(geo_json,f)
            self.uri = r'data/json_to_load_from_shp.geojson'
            self.GeojsonToArray(request=False)

    def CsvToArray(self,x,y,header,output_geojson=None):
        """Convert Csv to array.

        Args:
            x (str): Field name for X in csv.
            y (str): Field name for Y in csv.
            header (bool, optional): Whether csv file contains a header. Defaults to True.
            output_geojson (str,optional): File path to output geojson for csv. Defaults to None.
        """
        with open(self.uri,'r',encoding='utf8') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            i = 0
            geojson = dict()
            geojson['type'] = 'FeatureCollection'
            geojson['features'] = []
            for row in reader:
                if i == 0:
                    if header == True:
                        fields = row
                        x_index = fields.index(x)
                        y_index = fields.index(y)
                    else:
                        fields = ['Field_'+ str(i) for i in range(len(row))+1]
                    i += 1
                else:
                    record = dict()
                    record['type'] = 'Feature'
                    record['properties'] = dict(zip(fields,row))
                    record['geometry'] = dict()
                    record['geometry']['type'] = 'Point'
                    record['geometry']['coordinates'] = [row[x_index],row[y_index]]
                    geojson['features'].append(record)

            
            if os.path.exists(r'data/json_to_load_from_csv.geojson') == True:
                os.remove(r'data/json_to_load_from_csv.geojson')
            with open(r'data/json_to_load_from_csv.geojson','w') as f:                
                json.dump(geojson,f)
            
            if output_geojson is not None:
                with open(output_geojson,'w') as f:
                    json.dump(output_geojson,f)
            self.uri = r'data/json_to_load_from_csv.geojson'
            self.GeojsonToArray(request=False)
        
    def ToShp(self,out):
        """Convert Geo class to shapefile.

        Args:
            out (str): File path to save shp.
        """
        w = shapefile.Writer(out)
        for field in self.attributes:
            w.field(field,'C')
        for row in self.data:
            w.record(row[2:])
            w.point(float(row[0]),float(row[1]))
        
        w.close()


    def show(self, map=None, top = 0, kernel = 'folium'):
        """Draw the class object on the map with Folium.

        Args:
            map (Folium map object, optional): If set to None, the function will create a new map object. If given the map object, the layer will be drawn on the map. Defaults to None.
            top (int): The top number of records will be drawn on map. If top is set to 0, then all records will be drawn. Defaults to 0.
        """
        if top != 0:
            data = self.data[0:top]
        else:
            data = self.data
        if map == None:

            if kernel == 'folium':
                m = folium.Map(location=[data[0][1],data[0][0]])
                for record in data:
                    folium.Marker([record[1],record[0]]).add_to(m)
                display(m)
            if kernel == 'ipyleaflet':
                m = ipyleaflet.Map(center=[data[0][1],data[0][0]])
                markers = []
                for record in data:
                    marker = ipyleaflet.Marker(location=([record[1],record[0]]))
                    markers.append(marker)
                layer_group = ipyleaflet.LayerGroup(layers=(markers))
                m.add_layer(layer_group)
        else:
            markers = []
            for record in data:
                if kernel == 'folium':
                    folium.Marker([record[1],record[0]]).add_to(map)
                if kernel == 'ipyleaflet':
                    marker = ipyleaflet.Marker(location=([record[1],record[0]]))
                    markers.append(marker)
            layer_group = ipyleaflet.LayerGroup(layers=(markers))
            map.add_layer(layer_group)


class Map(ipyleaflet.Map):
    def __init__(self,**kwargs):
        """Map class
        """
        if "center" not in kwargs:
            kwargs["center"] = [40,-100]
        if "zoom" not in kwargs:
            kwargs['zoom'] = 4
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(**kwargs)

        if "height" not in kwargs:
            self.layout.height = "600px"
        else:
            self.layout.height = kwargs['height']

        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="bottomright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        main_toolbar(self)

        if "google_map" not in kwargs or kwargs["google_map"] == "ROADMAP":
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Maps"
            )
            self.add_layer(layer)
        elif kwargs["google_map"] == "HYBRID":
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Satellite"
            )
            self.add_layer(layer)
    
        if 'in_csv' in kwargs:
            in_csv = kwargs['in_csv']
            x = kwargs['x']
            y = kwargs['y']
            header = kwargs['header']
            self.add_points_from_csv(in_csv,x,y,header)

    def add_points_from_csv(self,in_csv,x,y,header):
        """[summary]

        Args:
            in_csv (str): File path to csv file.
            x (str): Field name for X in csv.
            y (str): Field name for Y in csv.
            header (bool, optional): Whether csv file contains a header. Defaults to True.
        """
        with open(in_csv,encoding='utf8') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            i = 0
            markers = []
            for row in reader:
                if i == 0:
                    if header == True:
                        fields = row
                        x_index = fields.index(x)
                        y_index = fields.index(y)
                    i += 1
                else:
                    markers.append(ipyleaflet.Marker(location=(row[y_index],row[x_index])))
            marker_cluster = ipyleaflet.MarkerCluster(markers=markers)
            self.add_layer(marker_cluster)