import settings as sgs
from framer import *
import datetime
import imageio
import signal
import numpy as np


def handler(signum, frame):
    """ Error handling """
    
    # Text of error handling
    raise Exception("| end of time")
    
    
def screenshot(j, df_trips, df_flux):
    """ Returns a screenshot in png format of the desired frame """
    
    # Compute absolute time
    current_time = sgs._start_time + datetime.timedelta(minutes=(np.around(60/sgs._hourly_rate))*j)
    
    # Using the go_frame function, create a png image representing the simulation at the given time
    go_frame((j, current_time), df_trips, df_flux)
    print('·',end='')
    
    return True


def serial_framer(begin, end, df_trips, df_flux):
    """ This function will automatically create snapshots until it fails """
    
    # Initialize variable
    failed_at = None
    
    # Iterate over the frame times
    for j in range(begin, end):
        
        # Set the maximal time of computation at 30 seconds
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(30)
        
        # Try to create a png snapshot of the simulation at the given time
        try:
            print(j,end='')
            screenshot(j, df_trips, df_flux)
            
        # If the time of computation exceeds 30 seconds, we assume that the operation is somehow blocked
        except Exception as e :
            
            # Print the exception handling message
            print(e)
            
            # Store carefully the frame which couldn't be created and return it
            failed_at = j
            return failed_at
        
    return end


def coach(df_trips, df_flux, begin = 0, end = sgs._simulation_duration):
    """ Calls the serial framer each time he fails until the work is done """
    
    # First initialisation of the maximal time of computation to 30 seconds
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    
    # Iterate until the end frame is finally created
    while begin < end :
        
        # Create frames until the serial framer fails. Then store the last frame which the
        # serial framer attempted to create and fix it as the next first frame to be created
        # in the next iteration
        last = serial_framer(begin, end, df_trips, df_flux)
        begin = last
    
    print(end)
    
    return True


def movie_maker(begin = 0, end = sgs._simulation_duration):
    """ Creates a mp4 movie from the png frames of the simulation """
    
    # Initialize variable
    filenames = []
    
    # Load all png images of the simulation
    for i in range(end - begin):
        filenames.append(sgs._png_folder + "frame_{:0>5}.png".format(i))
    
    # Create a mp4 movie from all snapshots
    with imageio.get_writer(sgs._mp4_folder + 'movie.mp4', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    return True

