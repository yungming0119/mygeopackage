import os
import ipywidgets as widgets
from ipyleaflet import WidgetControl, basemaps
from ipyfilechooser import FileChooser
from IPython.display import display
import mygeopackage
import folium

def main_toolbar(m):

    padding = "0px 0px 0px 5px"  # upper, right, bottom, left

    toolbar_button = widgets.ToggleButton(
        value=False,
        tooltip="Toolbar",
        icon="wrench",
        layout=widgets.Layout(width="28px", height="28px", padding=padding),
    )

    close_button = widgets.ToggleButton(
        value=False,
        tooltip="Close the tool",
        icon="times",
        button_style="primary",
        layout=widgets.Layout(height="28px", width="28px", padding=padding),
    )    

    toolbar = widgets.HBox([toolbar_button])

    def close_click(change):
        if change["new"]:
            toolbar_button.close()
            close_button.close()
            toolbar.close()
            
    close_button.observe(close_click, "value")

    rows = 2
    cols = 2
    grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="62px"))

    icons = ["folder-open", "map", "gears", "question"]

    for i in range(rows):
        for j in range(cols):
            grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                        layout=widgets.Layout(width="28px", padding="0px"))

    toolbar = widgets.VBox([toolbar_button])

    def toolbar_click(change):
        if change["new"]:
            toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
        else:
            toolbar.children = [toolbar_button]
        
    toolbar_button.observe(toolbar_click, "value")

    toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")

    m.add_control(toolbar_ctrl)

    output = widgets.Output()
    output_ctrl = WidgetControl(widget=output, position="topright")

    buttons = widgets.ToggleButtons(
        value=None,
        options=["Apply", "Reset", "Close"],
        tooltips=["Apply", "Reset", "Close"],
        button_style="primary",
    )
    buttons.style.button_width = "80px"

    data_dir = os.path.abspath('./data')

    fc = FileChooser(data_dir)
    fc.use_dir_icons = True
    fc.filter_pattern = ['*.shp', '*.geojson']

    filechooser_widget = widgets.VBox([fc, buttons])

    def button_click(change):
        if change["new"] == "Apply" and fc.selected is not None:
            if fc.selected.endswith(".shp"):
                #m.add_shapefile(fc.selected, layer_name="Shapefile")
                geo = mygeopackage.Geo(fc.selected,request=False,file_type='shp')
                geo.show(map=m,kernel='ipyleaflet')
            elif fc.selected.endswith(".geojson"):
                #m.add_geojson(fc.selected, layer_name="GeoJSON")
                geo = mygeopackage.Geo(fc.selected,request=False)
                geo.show(map=m,kernel='ipyleaflet')
        elif change["new"] == "Reset":
            fc.reset()
        elif change["new"] == "Close":
            fc.reset()
            m.remove_control(output_ctrl)
    buttons.observe(button_click, "value")     

    dropdown = widgets.Dropdown(
        options=['Road','Satellite'],
        value = 'Road',
        layout=widgets.Layout(width="200px")
    )
    basemap_widget = widgets.HBox([dropdown])

    def dropdown_changed(change):
        origin_basemap = lambda layer: 0 if len(layer) == 1 else 1
        if change['new'] == 'Road':
            m.substitute_layer(m.layers[origin_basemap(m.layers)],basemaps.Esri.WorldStreetMap)
        elif change['new'] == 'Satellite':
            m.substitute_layer(m.layers[origin_basemap(m.layers)],basemaps.Esri.WorldImagery)
        m.remove_control(output_ctrl)
    dropdown.observe(dropdown_changed,"value")

    def tool_click(b):    
        with output:
            output.clear_output()
            if b.icon == "folder-open":
                display(filechooser_widget)
                m.add_control(output_ctrl)
            elif b.icon == "gears":
                import whiteboxgui.whiteboxgui as wbt

                if hasattr(m, "whitebox") and m.whitebox is not None:
                    if m.whitebox in m.controls:
                        m.remove_control(m.whitebox)

                tools_dict = wbt.get_wbt_dict()
                wbt_toolbox = wbt.build_toolbox(
                    tools_dict, max_width="800px", max_height="500px"
                )

                wbt_control = WidgetControl(
                    widget=wbt_toolbox, position="bottomright"
                )                

                m.whitebox = wbt_control
                m.add_control(wbt_control)
            elif b.icon == "map":
                display(basemap_widget)
                m.add_control(output_ctrl)



    for i in range(rows):
        for j in range(cols):
            tool = grid[i, j]
            tool.on_click(tool_click)

def ml_tool():

    #Read Data
    data_dir = os.path.abspath('./data')

    fc = FileChooser(data_dir)
    fc.use_dir_icons = True
    fc.filter_pattern = ['*.shp', '*.geojson']

    button = widgets.Button(description='Read Data')
    def button_click(change):
        m = folium.Map(zoom_start=15)
        geo = []

        if fc.selected is not None:
            if fc.selected.endswith(".shp"):
                geo = mygeopackage.Geo(fc.selected,request=False,file_type='shp')
                #geo.show(map=m)
            elif fc.selected.endswith(".geojson"):
                geo = mygeopackage.Geo(fc.selected,request=False)
                #geo.show(map=m)
        analysis(m,geo)
        #display(m)

    button.on_click(button_click)     
    filechooser_widget = widgets.VBox([fc, button])
    display(filechooser_widget)

def analysis(m,geo):
    #Data Preprocessing
    field_select = widgets.Select(
        options = list(zip(geo.attributes,range(2,len(geo.attributes)+2))),
        description = "fields"
    )
    lr_button = widgets.Button(description='Apply')
    lr_tool = widgets.HBox([field_select,lr_button])
    lr_area = widgets.VBox([widgets.Label(value='Standardized Normalization'),lr_tool])

    def lr_click(change):
        if field_select.value is not None:
            import mygeopackage.pproc
            mygeopackage.pproc.standardNormalization(geo,field_select.value)
            print(geo.data[:,field_select.value])
    lr_button.on_click(lr_click)

    #Unsupervised Machine Learning
    style = {'description_width': 'initial'}
    n_text = widgets.IntText(value=2,description='Desired Clusters',style=style)
    field_multiple = widgets.SelectMultiple(
        options = list(zip(['X','Y',*geo.attributes],range(0,len(geo.attributes)+2))),
        description = "Fields"
    )
    index_field = widgets.Select(
        options = list(zip(geo.attributes,range(2,len(geo.attributes)+2))),
        description = "Identifier"
    )
    k_means_button = widgets.Button(description='Apply')
    k_means_tool = widgets.HBox([n_text,field_multiple,index_field])
    k_means_area = widgets.VBox([widgets.Label(description='K_Means'),k_means_tool,k_means_button])

    def k_means_click(change):
        
        import mygeopackage.unsupervised
        if field_multiple.value is not None:
            clusters = mygeopackage.unsupervised.Cluster(geo.data)
            mygeopackage.unsupervised.k_means(n_text.value,field_multiple.value,clusters,index_field.value)
            clusters.show(map=m)

    k_means_button.on_click(k_means_click)

    eps_text = widgets.Text(value='0.5',description="EPS")
    min_samples = widgets.IntText(value=5,description="Min_Samples")
    dbscan_button = widgets.Button(description="Apply")
    dbscan_tool = widgets.HBox([eps_text,min_samples,field_multiple,index_field])
    dbscan_area = widgets.VBox([widgets.Label(description="DBSCAN"),dbscan_tool,dbscan_button])

    def dbscan_click(change):
        import mygeopackage.unsupervised
        if field_multiple.value is not None:
            clusters = mygeopackage.unsupervised.Cluster(geo.data)
            mygeopackage.unsupervised.dbscan(float(eps_text.value),min_samples.value,field_multiple.value,clusters,index_field.value)
            clusters.show(map=m)

    dbscan_button.on_click(dbscan_click)
    accordion = widgets.Accordion(children=[k_means_area,dbscan_area])
    accordion.set_title(0,'K Means')
    accordion.set_title(1,'DBSCAN')
    #Regression
    dependent_field = widgets.Select(
        options = list(zip(['X','Y',*geo.attributes],range(0,len(geo.attributes)+2))),
        description = "Dependent Variable",
        style = style
    )
    independent_fields = widgets.SelectMultiple(
        options = list(zip(['X','Y',*geo.attributes],range(0,len(geo.attributes)+2))),
        description = "Independent Variable",
        style=style
    )
    regression_button = widgets.Button(description="Apply")
    regression_tool = widgets.HBox([dependent_field,independent_fields,index_field])
    regression_area = widgets.VBox([widgets.Label(description="Ordinary Least Square"),regression_tool,regression_button])
    
    def regression_click(change):
        import mygeopackage.regression
        if dependent_field.value is not None:
            reg_results = mygeopackage.regression.Regression()
            reg_results = mygeopackage.regression.ols(geo,dependent_field.value,independent_fields.value,index_field.value)
            reg_results.show(map=m)
            print('R2 Score: '+ str(reg_results.score))

    regression_button.on_click(regression_click)

    tab = widgets.Tab()
    tab_contents = ['Data Preprocessing','Unsupervised','Regression']
    tab.set_title(0,'Data Preprocessing')
    tab.set_title(1,'Unsupervised')
    tab.set_title(2,'Regression')
    tab.children = [lr_area,accordion,regression_area]
    display(tab)