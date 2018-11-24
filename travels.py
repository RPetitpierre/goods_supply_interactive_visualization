import settings as sgs
import numpy as np
import pandas as pd
from scipy import stats


def compute_travel_time(start_long,start_lat,arrival_long,arrival_lat):
    """ Compute the mean travel time (in 10Min frames) for an euclidian distance """
    
    # Absolute horizontal distance
    horiz = abs(start_long - arrival_long)
    
    # Absolute vertical distance
    verti = abs(start_lat - arrival_lat)
    
    # Convert map distance to real kilometric distance
    convert_to_km = 68.671
    
    # Compute the euclidian distance which is traveled in the hourly rate (here 4 per hour)
    euclidian_kmp_hourly_rate = sgs._euclidian_kmph / sgs._hourly_rate
    
    # Compute the travel time (distance in km / km per hourly rate)
    travel_time = np.sqrt(horiz*horiz + verti*verti)*convert_to_km / euclidian_kmp_hourly_rate
    
    # Returns the rounded travel time
    return int(np.around(travel_time, decimals = 0))


def compute_departures(flux):
    """ Compute the number of departing trains a day. """
    
    # Transform the yearly units on the map in ktons
    ktons_a_year = flux * sgs._ktons_per_unit
    
    # Compute the number of trains/boats necessary to transport the goods
    trains_a_year = ktons_a_year / sgs._ktons_per_train
    
    # Round the result and return it
    return int(np.around(trains_a_year, decimals = 0))


def create_travels(travel_time, flux):
    """ Create virtual train travel, in function of the amount of coal transported on the line
        and in function of the duration of the travel """
    
    # Trains/boats are normally distributed over the time range of the simulation
    normal_distribution = np.random.randint(low = 0, high = (len(sgs._time_range))-1,
                                            size = compute_departures(flux))
    
    # Convert the distribution in time format
    departure_times = sgs._time_range[normal_distribution]
    
    # Iterate over all travels
    for i, time in enumerate(normal_distribution):
        
        # If the time of arrival overpass the time range, reajust it 
        if time + travel_time >= len(sgs._time_range):
            normal_distribution[i] = time + travel_time - len(sgs._time_range)
        
        # Else, just deduce the arrival time from the departure time and the duration of the trip
        else :
            normal_distribution[i] = time + travel_time
    
    # Match values of arrival time with the time distribution
    arrival_times = sgs._time_range[normal_distribution]
    
    return departure_times, arrival_times


def create_timetable(df_flux):
    """ Create a complete timetable of boats and trains over the whole year, according to the
        importance of each flux """
    
    # Initialize variables
    from_city, to_city = [], []
    from_time, to_time = [], []
    isnaval, coal_type = [], []
    
    # Iterate over all flux rows
    for ind, row in df_flux.iterrows():
        
        # Initialize loop variables
        N, proba_map = sgs._Ntypes_production, []
        
        # If the naval mode is enabled, we have twice more types of flux
        if sgs._enable_Naval : N *= 2
        
        # Compute the flux types distribution
        for i in range(6, 6+N) :
            proba_map.append(row[i] / row['flux'])
        
        # Create an array with numbers arranged from 0 to N (N being the number of flux types)
        xk = np.arange(N)
        
        # Create a subclassifier in function of each different type
        custm = stats.rv_discrete(name = 'custm', values = (xk, proba_map))
        custm.rvs(size = 1)
        
        # Create the travels corresponding to the flux
        departure_times, arrival_times = create_travels(
            compute_travel_time(row['from_longitude'], row['from_latitude'],
                                row['to_longitude'], row['to_latitude']), row['flux'])
        
        # Iterate over trips in this flux
        for i in range(len(departure_times)):
            
            # Catch information about departure and arrival
            from_city.append(row['from_city'])
            to_city.append(row['to_city'])
            from_time.append(departure_times[i])
            to_time.append(arrival_times[i])
            
            # Class the trip according to the types distribution
            coal_type_ = custm.rvs(size = 1)
            coal_type.append(coal_type_[0]+1)
            
            # If the naval mode is enabled, check the type
            if (sgs._enable_Naval):
                if coal_type_+1 > N/2: isnaval.append(1)
                else : isnaval.append(0)
           
            # Else, we don't need to check the type and just add a zero
            else : isnaval.append(0)
    
    # Prepare the columns of the dataframe
    dict_trains = {
        'from_city' : from_city,
        'to_city' : to_city,
        'departure_time' : from_time,
        'arrival_time' : to_time,
        'coal_type' : coal_type,
        'is_naval' : isnaval
    }
    
    # Convert the dictionary to a pandas dataframe
    df_trains = pd.DataFrame.from_dict(dict_trains)
    
    return df_trains

