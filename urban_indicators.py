# Author: Sara Todorovic
# January 2019
# Automating GIS processes 2018, University of Helsinki


# Function to get a geodataframe from a list of placenames
def urban_gdf(placenames):
    """
    Function for downloading a geodataframe from OSM from a list of places.

    Parameters
    ----------
    placenames: <list>
        List of places.
    Returns
    -------
    <geodataframe>
        Geodataframe containing geometry of the places.
    """ 
    # Using the function:
    # Fetch geodataframe from OSM
    gdf = ox.gdf_from_places(placenames)
    # Return geodataframe
    return gdf

# Function to download the networks for a given list of placenames
def urban_getNetwork(placenames, nwtype):
    """
    Function for downloading networks as a list of graphs from OSM for a given list of place names

    Parameters
    ----------
    placenames: <list>
        List of places.
    nwtype: <string>
        Defines the network type that is downloaded from OSM.
    Returns
    -------
    <list>
        List containing graphs fetched from OSM.
    """ 
    # Using the function: 
    
    # Empty list for the graphs that will be downloaded
    places_graph = []
    
    # For each place in the list of given placenames,
    for place in placenames:
        # Fetch the graph with the network type of choice
        graph = ox.graph_from_place(place, network_type = nwtype)
        # Add to the list
        places_graph.append(graph)
        
    # Return the list containing the graphs    
    return places_graph 

# Function to visualise the street networks for a given list of placenames            
def urban_visNetwork(placenames, nwtype):
    # For each place in a list of placenames
    for place in placenames:
        
        # Use function urban_getNetwork to fetch the graphs for each place in the list
        places = urban_getNetwork(placenames)
        
        # Create the graphs
        graph = ox.graph_from_place(place, network_type = nwtype)
        
        # Print the placename for each graph
        print(graph)
        
        # Return the street network
        fig, ax = ox.plot_graph(ox.project_graph(graph), node_size=0)
        
# Function to calculate and visualise bearings of street network as graphs
def urban_bearings(placenames, nwtype, color):
    """
    Function for visualising the street network edge bearings as graphs.
    Produces as many graphs as there as components in the input list.

    Parameters
    ----------
    placenames: <list>
        List of places.
    nwtype: <string>
        Defines the network type that is downloaded from OSM.
    color: <string>
        Defines the color of the graph.
    Returns
    -------
    <graph>
        Graphs of the street network edge bearings.
    """ 
    # Using the function:
    
    # For each place in the list of given placenames,
    for place in placenames:
        
        # Create a variable G where you store the graph from the network
        G = ox.graph_from_place(place, network_type=nwtype)
        
        # Add edge bearings to G
        G = ox.add_edge_bearings(G)
        
        # Calculate edge bearings from the graph's edges
        bearings = pd.Series([data['bearing'] for u, v, k, data in G.edges(keys=True, data=True)])
        
        # Create a histogram and define parameters
        ax = bearings.hist(bins=30, zorder=2, alpha=0.8, color=color)
        
        # Set xlim as 360 (circle is 360 degrees)
        xlim = ax.set_xlim(0, 360)
        
        # Set the placename as the title of each individual graph in the list
        ax.set_title(place)
        
        # Show each graph
        plt.show()


# Function for visualising the street network edge bearings as polar plots
def urban_polarPlot(placenames, nwtype, color):
    """
    Function for visualising the street network edge bearings as polar plots,
    where the place's street network's edge bearings are spread as a circle of 0 to 360 degrees, 
    value indicating the orientation of the street.
    
    Produces as many polar plots as there as components in the input list.

    Parameters
    ----------
    placenames: <list>
        List of places.
    nwtype: <string>
        Defines the network type that is downloaded from OSM.
    color: <string>
        Defines the color of the graph.
    Returns
    -------
    <graph>
        Graphs of the street network edge bearings.
    """ 
    # Using the function:
    
    # For each place in the list of given placenames,
    for place in placenames:
        
        # Create a variable G where you store the graph from the network
        G = ox.graph_from_place(place, network_type=nwtype)
        # Add edge bearings to G
        G = ox.add_edge_bearings(G)
        # Calculate edge bearings from the graph's edges
        bearings = pd.Series([data['bearing'] for u, v, k, data in G.edges(keys=True, data=True)])
        
        # Create a numpy histogram with 360 degrees
        n = 30
        count, division = np.histogram(bearings, bins=[ang*360/n for ang in range(0,n+1)])
        division = division[0:-1]
        # Setting width to be visually nice
        width =  2 * np.pi/n
        # Set the projection to polar, and axis zero location and direction
        ax = plt.subplot(111, projection='polar')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction('clockwise')
        
        # Axis bars
        bars = ax.bar(division * np.pi/180 - width * 0.5 , count, width=width, bottom=0.0, color=color)
        ax.set_title(place, y=1.1)
        # Set x tick labels to North, East, South and West
        xticklabels = ['N', '', 'E', '', 'S', '', 'W', '']
        ax.set_xticklabels(labels=xticklabels)
        
        plt.show()
        
        

