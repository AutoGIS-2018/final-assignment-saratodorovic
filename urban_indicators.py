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
        
def urban_bearings(placenames):
    for place in placenames:
        G = ox.graph_from_place(place, network_type='drive')

        # Calculate edge bearings and visualize their frequency
        G = ox.add_edge_bearings(G)
        bearings = pd.Series([data['bearing'] for u, v, k, data in G.edges(keys=True, data=True)])
        ax = bearings.hist(bins=30, zorder=2, alpha=0.8, color="purple")
        xlim = ax.set_xlim(0, 360)
        ax.set_title(place)
        plt.show()

def urban_polarPlot(placenames):
    for place in placenames:
        G = ox.graph_from_place(place, network_type='drive')

        # Calculate edge bearings and visualize their frequency
        G = ox.add_edge_bearings(G)
        bearings = pd.Series([data['bearing'] for u, v, k, data in G.edges(keys=True, data=True)])
        
        n = 30
        count, division = np.histogram(bearings, bins=[ang*360/n for ang in range(0,n+1)])
        division = division[0:-1]
        width =  2 * np.pi/n
        ax = plt.subplot(111, projection='polar')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction('clockwise')
        bars = ax.bar(division * np.pi/180 - width * 0.5 , count, width=width, bottom=0.0, color='purple')
        ax.set_title(place, y=1.1)
        plt.show()
        

