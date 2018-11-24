import folium
import settings as sgs
import numpy as np
from folium import plugins


def plot_cities_import_export(df):
    """ Function specialized in the creation of interactive map representing import/export """
    
    # Initialize parameters
    color = ''
    arg = 'import_export'
    df_ = df
    
    # Calculate net export
    df_[arg] = df['production'] - df['consumption']
    
    # Remove the cities whose net import-export is null
    df_ = df_[df_[arg]!=0]
    
    # Specify parameters of the folium map
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")

    # For each row in the data, add a circle marker
    for index, row in df_.iterrows():
                
        # If city is a net exporter
        if row[arg] > 0:
            
            # Generate a popup message that is shown on click
            popup = "{}<br> Net coal export: {} thousands tons"
            color = "#309632" # green (net exporter)
            
        # If city is a net importer
        else:
            # Generate a popup message that is shown on click
            popup = "{}<br> Net coal import: {} thousands tons"
            color = "#BA160C" # red (net importer)
        
        # Display the popup message
        popup = popup.format(row["city_name"],int(abs(row[arg])*sgs._ktons_per_unit))
        
        # Define the radius of the circle so that its surface is proportional the the 
        # scalar (import/export tons)
        radius = np.sqrt((abs(row[arg])))/np.pi
        
        # Add circle marker to the map
        folium.CircleMarker(location = (row["latitude"],row["longitude"]),
                            radius = radius,
                            color = color,
                            popup = popup,
                            fill = True).add_to(folium_map)
    
    # Enable folium measure tool
    measure_control = plugins.MeasureControl(primary_length_unit='kilometers',
                                             primary_area_unit='sqkilometers')
    
    # Enable folium fullscreen plugin
    fullscreen = plugins.Fullscreen()
    
    # Add plugins to the map
    measure_control.add_to(folium_map)
    fullscreen.add_to(folium_map)
    
    return folium_map


def plot_cities_transiting_flux(df):
    """ Function specialized in the creation of interactive maps representing goods transit """
    
    # Initialize parameters
    color = ''
    arg = 'transiting_flux'
    df_ = df
    
    # Remove the cities whose net transiting flux is null
    df_ = df_[df_[arg]!=0]

    # Specify parameters of the folium map
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")

    # For each row in the data, add a cicle marker
    for index, row in df_.iterrows():
        
        # Generate a popup message that is shown on click and display it
        popup = "{}<br> Arriving coal: {} thousands tons<br>"
        popup += "Departing coal: {} thousands tons<br> Total coal transit: {} thousands tons"
        popup = popup.format(row["city_name"],
                             int(abs(row['arriving_flux'])*sgs._ktons_per_unit),
                             int(abs(row['departing_flux'])*sgs._ktons_per_unit),
                             int(abs(row['transiting_flux'])*sgs._ktons_per_unit))
        
        # Set colour to violet
        color = '#A85CE8' # violet
        
        # Define the radius of the circle so that its surface is proportional the the 
        # scalar (transit)        
        radius = np.sqrt((abs(row[arg])))/np.pi
        
        # Add circle marker to the map
        folium.CircleMarker(location = (row["latitude"],row["longitude"]),
                            radius = radius,
                            color = color,
                            popup = popup,
                            fill = True).add_to(folium_map)
        
    # Enable folium measure tool
    measure_control = plugins.MeasureControl(primary_length_unit='kilometers',
                                             primary_area_unit='sqkilometers')
    
    # Enable folium fullscreen plugin
    fullscreen = plugins.Fullscreen()
    
    # Add plugins to the map
    measure_control.add_to(folium_map)
    fullscreen.add_to(folium_map)
    
    return folium_map


def plot_cities_production(df):
    """ Function specialized in the creation of interactive maps representing production centers """

    # Initialize parameters
    arg = 'production'
    df_ = df
    
    # Remove the cities whose net production is null
    df_ = df_[df_[arg]!=0]
    
    # Specify parameters of the folium map
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")

    # For each row in the data, add a cicle marker
    for index, row in df_.iterrows():
        
        # Generate a popup message that is shown on click.
        popup = "{}<br> {}<br>Coal production: {} thousands tons"
        
        # Set the colour to the one which is specified in the settings folder
        color = sgs._production_colors[int(row['type_production'])-1]
        
        # Display the popup message
        popup = popup.format(row["city_name"],sgs._descr[int(row['type_production'])-1],
                                                        int(abs(row[arg])*sgs._ktons_per_unit))
        
        # Define the radius of the circle so that its surface is proportional the the scalar (production)
        radius = np.sqrt((abs(row[arg])))/np.pi
        
        # Add circle marker to the map
        folium.CircleMarker(location = (row["latitude"],row["longitude"]),
                            radius = radius,
                            color = color,
                            popup = popup,
                            fill = True).add_to(folium_map)
        
    # Enable folium measure tool
    measure_control = plugins.MeasureControl(primary_length_unit='kilometers',
                                             primary_area_unit='sqkilometers')
    
    # Enable folium fullscreen plugin
    fullscreen = plugins.Fullscreen()
    
    # Add plugins to the map
    measure_control.add_to(folium_map)
    fullscreen.add_to(folium_map)
    
    return folium_map


def plot_cities(df, arg):
    """ Generalist function for creating interactive folium maps """
    
    # Store the different messages and colours corresponding to the various data
    # which could be plotted
    dict_plot_cities = {
        'consumption' : ["{}<br> Coal consumption: {} thousands tons",'#E37222'],
        'production' : ["{}<br> Coal production: {} thousands tons",'#E8DC5C'],
        'arriving_flux' : ["{}<br> Arriving coal: {} thousands tons",'#5CE8C2'],
        'departing_flux' : ["{}<br> Departing coal: {} thousands tons",'#3893E8']
    }
    
    # Initialize parameters
    color = ''
    df_ = df
    
    # Remove the cities whose net value is null
    df_ = df_[df_[arg]!=0]
    
    # Specify parameters of the folium map
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")

    # For each row in the data, add a cicle marker
    for index, row in df_.iterrows():
        
        # Catch the popup message matching the data which is plotted
        popup = dict_plot_cities[arg][0]
        color = dict_plot_cities[arg][1]
        
        # Display the popup message
        popup = popup.format(row["city_name"],int(abs(row[arg])*sgs._ktons_per_unit))
        
        # Define the radius of the circle so that its surface is proportional the the scalar
        radius = np.sqrt((abs(row[arg])))/np.pi
        
        # Add circle marker to the map
        folium.CircleMarker(location = (row["latitude"],row["longitude"]),
                            radius = radius,
                            color = color,
                            popup = popup,
                            fill = True).add_to(folium_map)
        
    # Enable folium measure tool
    measure_control = plugins.MeasureControl(primary_length_unit='kilometers',
                                             primary_area_unit='sqkilometers')
    
    # Enable folium fullscreen plugin
    fullscreen = plugins.Fullscreen()
    
    # Add plugins to the map
    measure_control.add_to(folium_map)
    fullscreen.add_to(folium_map)
    
    return folium_map

