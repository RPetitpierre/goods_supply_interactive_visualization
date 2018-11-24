import folium
import settings as sgs
import numpy as np


def get_beautiful_base_image_map(df_flux, thin=False):
    """ Create the beautiful folium map containing routes, with blur effect """
    
    # Initialize folium map parameters
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")
    
    # From outer to inner, establish a beautiful shading of colors and opacities in order
    # to create a lightning effect
    colors = ['#FFCB00','#FFD325','#FDFAF1']
    weight = 1
    
    # The thin mode allow to draw a very light network, which is useful if you want to add
    # other information of the map in order to avoid to overload the representation
    if thin :
        opacities = [.12, .16, .55]
        weight = 1/20
    else :
        opacities = [.18, .23, .8]
        weight = 1/5
        
    # The process is doubled because of a bug from folium which sometimes doesn't draw the line    
    for j in range(2):
        
        # Iterate on all routes to draw
        for ind_, row in df_flux.iterrows():
            
            # Iterate over the successive layers of colors/weights/opacities which result in the lightning effect
            for i in range(len(colors)):
                
                # Add a line on the folium map
                folium.PolyLine(locations = [[row[4], row[5]],
                                             [row[1], row[2]]],
                                color = colors[i],
                                opacity = float(opacities[i]),
                                weight = np.log2(row['flux'])*(len(colors)-i)*weight).add_to(folium_map)
            
    return folium_map


def get_beautiful_tricolor_base_image_map(df_flux):
    """ Create the beautiful folium map containing routes, with blur effect. In this variant,
        the naval trade routes will be displayed in blue. Land+naval routes will be displayed
        in green """
    
    # This tricolor representation only make sense if the naval mode is enabled
    if sgs._enable_Naval :
        
        # Initialize folium map parameters
        folium_map = folium.Map(location = sgs._location_map,
                                zoom_start = sgs._zoom_map,
                                tiles = "CartoDB dark_matter")
    
        # From outer to inner, establish a beautiful shading of colors and opacities in order
        # to create a lightning effect
        colors = [['#FFCB00','#FFD325','#FDFAF1'], # gold for land routes
                  ['#0092FF', '#25C5FF','#CAE9FF'], # blue for naval routes
                  ['#00CE18','#25CE39','#B4E1B9']] # green for land+naval routes
        opacities = [.18, .23, .8]
        
        # The process is doubled because of a bug from folium which sometimes doesn't draw the line    
        for j in range(2):
            
            # Iterate on all routes to draw
            for ind_, row in df_flux.iterrows():
            
                # Select land flux, naval flux or heterogenous flux
                if sum(row[6:6+sgs._Ntypes_production]) > 0 :
                    if sum(row[16:16+sgs._Ntypes_production]) > 0: I = 2
                    else : I = 0
                else : I = 1
                    
                # Iterate over the successive layers of colors/weights/opacities which result in the lightning effect    
                for i in range(len(colors[I])):
                    
                    # Add a line on the folium map
                    folium.PolyLine(locations = [[row[4], row[5]],
                                                 [row[1], row[2]]],
                                    color = colors[I][i],
                                    opacity = float(opacities[i]),
                                    weight = np.log2(row['flux'])*(len(colors[I])-i)/5).add_to(folium_map)
    
    # If the naval mode is not enabled, we just call the classical function
    else :
        folium_map = get_beautiful_base_image_map(flux)
    
    return folium_map


def get_beautiful_base_image_map_by_route_category(df_flux, mode):
    """ Create the beautiful folium map containing routes, with blur effect. In this variant,
        depending on the mode ('naval' or 'land'), only land or naval routes will be displayed """
    
    # Initialize folium map parameters
    folium_map = folium.Map(location = sgs._location_map,
                            zoom_start = sgs._zoom_map,
                            tiles = "CartoDB dark_matter")
        
    # This tricolor representation only make sense if the naval mode is enabled
    if sgs._enable_Naval :
        
        # Initialize variable
        colors = []
    
        # From outer to inner, establish a beautiful shading of colors and opacities in order
        # to create a lightning effect
        if mode == 'naval' :
            colors = ['#0092FF', '#25C5FF','#CAE9FF'] # blue for naval routes
        elif mode == 'land' :
            colors = ['#FFCB00','#FFD325','#FDFAF1'] # gold for land routes
        else : 
            print("ERROR : mode should be either 'land' or 'naval'.")
            folium_map = get_beautiful_base_image_map(flux)
        
        opacities = [.18, .23, .8]
        
        # The process is doubled because of a bug from folium which sometimes doesn't draw the line    
        for j in range(2):
            
            # Iterate on all routes to draw
            for ind_, row in df_flux.iterrows():
                
                # Initialize variable
                is_of_route_category = False
                
                # Test if the route is a land route 
                if (sum(row[6:6+sgs._Ntypes_production]) > 0) & (mode == 'land') :
                    is_of_route_category = True
                    
                # Test if the route is a naval route
                elif (sum(row[16:16+sgs._Ntypes_production]) > 0) & (mode == 'naval') :
                    is_of_route_category = True
                
                # Route is only plotted if it is of the wished category
                if is_of_route_category:
                    
                    # Iterate over the successive layers of colors/weights/opacities which result in the lightning effect    
                    for i in range(len(colors)):
                    
                        # Add a line on the folium map
                        folium.PolyLine(locations = [[row[4], row[5]],
                                                     [row[1], row[2]]],
                                        color = colors[i],
                                        opacity = float(opacities[i]),
                                        weight = np.log2(row['flux'])*(len(colors)-i)/5).add_to(folium_map)
    
    # If the naval mode is not enabled, we just call the classical function
    else :
        print('ERROR : Naval mode should be enabled to use this function.')
        folium_map = get_beautiful_base_image_map(flux)
    
    return folium_map

