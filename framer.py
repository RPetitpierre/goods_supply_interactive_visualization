import settings as sgs
import numpy as np
from network import *
import folium
import signal
import io
from PIL import Image, ImageDraw, ImageFont


def get_path_progress(df_trips, image_time):
    """ Return a series of numbers between 0 and 1 indicating the percentage of 
        progress of each trip at the given time """
    
    df_progress = df_trips[["arrival_time","departure_time"]]
    duration = df_progress.arrival_time - df_progress.departure_time
    time_from_departure = image_time - df_progress.departure_time
    
    # Compute the percentage of progress and return it
    return (time_from_departure/duration)


def get_current_position(df_trips, progress):
    """ Return Latitude and Longitude for the 'current position' of each trip.
        Paths are assumed to be straight lines between start and end """
    
    # From depart and arrival latitude and longitude, as well as percentage of progress, 
    # compute the current latitude and longitude
    current_latitude = df_trips["from_latitude"]*(1-progress) + \
                       df_trips["to_latitude"]* progress
    current_longitude = df_trips["from_longitude"]*(1-progress) + \
                       df_trips["to_longitude"]* progress
    
    return current_latitude, current_longitude


def get_active_trips(image_time, df_trips):
    """ Return coordinates of all trips that have started and that are not yet been 
        completed at the given time """
    
    # Active trips are those whose departure time is already passed but whose arrival
    # time has not yet passed
    active_trips = df_trips[(df_trips["departure_time"] <= image_time)]
    active_trips = active_trips[(df_trips["arrival_time"] >= image_time)].copy()
    
    # Initialize variables
    current_latitude, current_longitude = [], []
    coal_type = []
    if (sgs._enable_Naval):
        isnaval = []
    
    # Iterate on all active trips
    for i in range(len(active_trips)):
        
        # Compute the percentage of completion of each trip
        progress = get_path_progress(active_trips.iloc[i], image_time)
        
        # Match this percentage of completion to extrapolate the current position
        # of the boat or of the train
        a, b = get_current_position(active_trips.iloc[i], progress)
        
        # Store the result
        current_latitude.append(a)
        current_longitude.append(b)
        
        # Extract the type of coal which is transported
        coal_type.append(active_trips.iloc[i]['coal_type'])
        
        # If the naval mode is enabled, a boolean defines if the trip is a naval 
        # or a land trip
        if (sgs._enable_Naval):
            isnaval.append(active_trips.iloc[i]['is_naval'])
    
    # Return all the information about the active trips
    if (sgs._enable_Naval):
        return current_latitude, current_longitude, coal_type, isnaval
    else :
        return current_latitude, current_longitude, coal_type

    
def get_image_map(frame_time, df_trips, df_flux):
    """Create the folium map for the given time """
    
    # Establish a base map depicting the network of trade routes
    folium_map = get_beautiful_base_image_map(df_flux, True)
    
    # If the naval mode is enabled
    if (sgs._enable_Naval):
        
        # Extract the information about the active trips, including if the trip is a land trip or a naval one
        current_latitude, current_longitude, coal_type, isnaval = get_active_trips(frame_time, df_trips)
        
        # Iterate on all active trips
        for i in range(len(current_longitude)):
            
            # As the naval mode is enabled in this case, we extend the colour palette
            production_colors = sgs._production_colors*2
            
            # Plot each naval trip as a triangle
            if (isnaval[i] == 1) :
                folium.RegularPolygonMarker(location=[current_latitude[i], current_longitude[i]],
                                            radius=2,
                                            number_of_sides = 3,
                                            color=production_colors[coal_type[i]-1],
                                            fill_color=production_colors[coal_type[i]-1]).add_to(folium_map)
                
            # Plot each land trip as a circle
            else:
                folium.CircleMarker(location=[current_latitude[i], current_longitude[i]],
                                    radius=1,
                                    color=production_colors[coal_type[i]-1],
                                    fill=True).add_to(folium_map)
    
    # If the naval mode is not enabled, this is much simpler
    else:
        
        # Extract the information about the active trips
        current_latitude, current_longitude, coal_type = get_active_trips(frame_time, df_trips)
        
        # Iterate on all active trips
        for i in range(len(current_longitude)):
            
            # Plot each trip as a circle
            folium.CircleMarker(location=[current_latitude[i], current_longitude[i]],
                                radius=1,
                                color=sgs._production_colors[coal_type[i]-1],
                                fill=True).add_to(folium_map)
    
    return folium_map

def go_frame(params, df_trips, df_flux):
    """ Generate the image frame from html, add annotations, and save image file in png """
    
    # Unpack parameters
    i, frame_time = params
    
    # Create the html map at the frame time, given the trips and flux data
    my_frame = get_image_map(frame_time, df_trips, df_flux)
    
    # Convert the html folium map to a png image
    png = my_frame._to_png(delay=6)
    
    # Load the png image in order to be able to modify it
    stream = io.BytesIO(png)
    image = Image.open(stream)
    draw = ImageDraw.Draw(image)
    
    # Load the font
    font = ImageFont.truetype(sgs._data_folder+"LibreBaskerville-Regular.otf", 30)
    
    # Add date and time of day text on the png image
    draw.text((20,image.height - 50), 
              "time: {}".format(frame_time),
              fill=(255, 255, 255), 
              font=font)
    
    # Save the png image
    draw = ImageDraw.Draw(image)
    image.save(sgs._png_folder + "frame_{:0>5}.png".format(i))
    
    return True
