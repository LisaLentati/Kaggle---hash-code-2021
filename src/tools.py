import numpy as np
import pandas as pd
from collections import Counter

def add_edge_count_col(paths, df_edges):
    """Adds the column 'counts' to df_edges. Indicating how many times each edge 
    appears in paths (i.e. a car goes through the edge).
    Return a df for which 'counts' > 0
    """

    # we flatten out all the paths into paths_list
    paths_list = list()
    for i in paths.keys():
        paths_list += paths[i]

    # we count the different elements of paths_list and create a pd.Series of it
    c = dict(Counter(paths_list))
    df_counts = pd.Series(c).reset_index(name='count')
    df_counts = df_counts.rename(columns={'index': 'name'})

    # we add the "counts" to the original df
    df_edges = pd.merge(df_edges, df_counts, how='left', on='name')
        
    return df_edges


def less_paths(paths, n):
    m = min(n, len(paths))

    new_paths = dict()
    for i in range(m):
        new_paths[i] = paths[i]

    return new_paths



def create_incoming_roads_count(df):
      
    return dict(df.groupby(by='to').size())

def create_incoming_nodes(df):
    incoming_roads = dict()
    for i, g in df.groupby(by='to')['from']:
        incoming_roads[i] = list(g)
    return incoming_roads

def create_distance_between_nodes(df):
    distance_between_nodes = dict()
    for row in df.values:
        leaving_node, incoming_node, _, lenght, _ = row
        distance_between_nodes[(leaving_node, incoming_node)] = lenght
    return distance_between_nodes


def create_paths_as_nodes(df, paths): 
    
    df_helper = df[['name', 'to']].copy()
    incoming_node_dict  = df_helper.set_index('name').to_dict()['to']

    paths_as_nodes = dict()
    for car_id in paths.keys():
        paths_as_nodes[car_id] = [incoming_node_dict[road] for road in paths[car_id]]

    return paths_as_nodes