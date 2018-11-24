# Goods supply interactive visualization
This program allow an interactive visualization of goods supply network. In our example, we wanted to represent the coal supply in the German Empire during the year 1881.

## Description of the files
### DH_map_V4.ipynb
Jupyter notebook containing the main program. This is where you will be able to obtain the different kinds of interactive map. Among them, the consumption of the cities, their production (which can also be displayed by type), the net import-export, the main transport hubs, etc. You will also be able to visualize the transport network. In addition, this is where you will be able to create a mp4 movie representing the flux of goods.
### settings.py
You will have to modify the global variables in this python file in order to run the program with your own data. See the detailed description of these parameters below.
### plot_cities.py
This python file contains all the useful functions to plot the interactive maps of cities.
* _plot_cities(df, arg)_ : Here you will have to input your merged pandas dataframe (see example in the .ipynb file) and simply specify the parameter ('consumption', 'production', 'arriving_flux' or 'departing_flux'.
* _plot_cities_production(df)_ : This sister function will display the production centers according the the production type (these parameters have to be specified in the settings.py)
* _plot_cities_transiting_flux(df)_ : This sister function will display the transport hubs.
* _plot_cities_import_export(df)_ : This sister function will display the net import-export.
### network.py
This python file will help you to display the network between cities. If the naval mode is enabled (see settings.py), you will be able to choose between 3 options :
* _get_beautiful_base_image_map(df_flux, thin=False)_ : Just displays the network in gold tone, independently on the fact that the route is naval of terrestrial. 
* _get_beautiful_tricolor_base_image_map(df_flux)_ : In this variant, the land trades routes will be displayed in gold, while naval trade routes will be displayed in blue. Routes which are both land & naval routes will be displayed in green.
* _get_beautiful_base_image_map_by_route_category(df_flux, mode)_ : Here, you will have to specify whether your want to display 'land' routes or 'naval' routes, in the _mode_ parameter.
### travels.py
This python file contains the necessary functions to create the simulation. It will thus create an artificial schedule of trains and boats to transport goods from one city to another, taking into account the quantity of goods to be transported over the specified period.
### framer.py
This file will allow you to create snapshots of the simulation at a given time.
### movie_maker.py
This file will create snapshots of the simulation for the entire duration specified in _settings.py_ and assemble them into an mp4 video that it will store in the "mp4" repository. Snapshots will be saved in the "png" repository.

## Settings
### Folders
Normally, you wouldn't have to change this, except if you gave different names to your repositories.
### Parameters
* __\_Ntypes_production__ : The number of different types of goods or of different regions of production.
* __\_enable_Naval__ : You can activate this parameter (_True_) if your transport routes can be naval, terrestrial or both. If you only want to work with land routes, just set this parameter to _False_. Note that this will duplicate the previous parameter, as each trade route will be able to convey the different types of goods either on land or on sea/river (or both).
* __\_production_colors__ : The color-code in which you want to display the various production types or production regions (or the different types of goods). Check www.color-hex.com if needed. Note that the color code should be in this format : '#A550FF'. In particular, the _#_ shouldn't be forgotten and the letters should be UPPERCASE.
* __\_descr__ : Textual description of the different types of goods or different regions of production.
* __\_ktons_per_unit__ : Fill this parameter if you have to convert the values from your csv. data to kilotons. If your data are already saved as kilotons, just set this parameter to _1_.
* __\_ktons_per_train__ : Please specify the number of kilotons of goods that a train or boat can carry, according to your model.
* __\_euclidian_kmph__ : The velocity as the crow flies of trains/boats in your model.
* __\_start_time__ : Start time and date of your simulation, in the following format : '1881-01-01 00:00:00'
* __\_hourly_rate__ : Smallest time unit of the simulation, in fraction of an hour. For example, enter _4_ for a simulation with quarter-hour accuracy and enter _0.5_ for a two-hour accuracy.
* __\_simulation_duration__ : Duration of the simulation. Change only the first two digits. For example, leaving the parameter _int(365\*24\*\_hourly\_rate)_, the simulation duration will be 365 days (24 hours a day).
* __\_time_range__ : Please consistently adapt this parameter to your previous decisions, if necessary change the starting data and the frequency.
* __\_location_map__ : Coordinates of the center of the map (check www.latlong.net if necessary).
* __\_zoom_map__ : Original zoom or dezoom of the map

You're basically done. Enter your dataset and the programm will do the rest !

## Dataset
The dataset should be in the very same csv format as our dataset (your can find it on this github, in the /data/ repository. Please keep the same columns and files names, or adapt them in the code. The only names you can change without causing any problems to the program will be the names of the production types columns.




