import pandas as pd

def init() :
    
    # Initialize global variables
    global _data_folder
    global _html_folder
    global _png_folder
    global _mp4_folder
    
    # Include the names of the repositories if necessary
    _data_folder = r'./data/'
    _html_folder = r'./html/'
    _png_folder = r'./png/'
    _mp4_folder = r'./mp4/'
    
    # Initialize global variables
    global _Ntypes_production
    global _enable_Naval
    global _production_colors
    global _descr
    global _ktons_per_unit
    global _ktons_per_train
    global _euclidian_kmph
    global _start_time
    global _hourly_rate
    global _simulation_duration
    global _time_range
    global _location_map
    global _zoom_map
    
    '''
    ###########################################################################################
    ·················· PARAMETERS TO COMPLETE IN ORDER TO FIT YOUR OWN MODEL ··················
    '''
    
    # The number of different types of goods or of different regions of production
    _Ntypes_production = 10

    # If some goods are transported by naval way (naval mode enabled => True, else => False)
    _enable_Naval = True

    # Please specify the colors (check www.color-hex.com if needed) in which you want to 
    # display the various production types or production regions
    _production_colors = ['#FF3FBD','#FF4141','#A550FF','#40EEBB','#3DFF40',
                          '#FFED43','#32E397','#2978FF','#FFAD32','#C7AC85']

    # Please provide the textual description you want to display for each production type
    _descr = ['Prussian coal from Upper Silesia','Prussian coal from Saarbrücken',
              'Prussian coal from Waldenburg','Prussian coal from the Ruhr',
              'Prussian coal from Hannover','Saxo-Prussian coal from Aachen,\nJbbenbüren, Zwickau or Plauen',
              'Moravian Coal', 'English Coal','Domestic turf', 'Bohemian turf']
    
    # If you need to convert the values from the table to display the kilotons
    _ktons_per_unit = 0.5 
    
    # The number of kilotons that a single train can carry
    _ktons_per_train = 0.33
    
    # The velocity on euclidian distance, in km per hour
    _euclidian_kmph = 60
    
    # Start_time of the mp4 simulation
    _start_time = pd.to_datetime('1881-01-01 00:00:00')
    
    # We set the rate of simulation the a quarter of hour (4 per hour)
    _hourly_rate = 12
    
    # In this example, we simulate 365 days of 24 hours, divided in 15-minutes intervalls.
    # This means that we simulate 365 days * 24 hours * 4 quarter hour
    _simulation_duration = int(365*24*_hourly_rate)
    
    # Time range of simulation
    _time_range = pd.date_range('1/1/1881', periods=_simulation_duration, freq='5Min')
    
    # Coordinates of the center of the map (check www.latlong.net if necessary)
    _location_map = [52, 12]
    
    # Original zoom or dezoom of the map
    _zoom_map = 6
    
    '''
    ###########################################################################################
    '''
    
    return True

