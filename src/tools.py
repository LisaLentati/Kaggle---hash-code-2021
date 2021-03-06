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


def create_random_node_order(df):
    
    rng = np.random.default_rng()

    schedule_order = list()
    
    for node in df['to'].unique():

        small_df = df.loc[df.to == node]

        edges_order = rng.permutation(small_df['name'].values)    
        schedule_order.append(list(edges_order))

    

    return  pd.DataFrame({'node': df['to'].values, 'order': schedule_order})


def less_paths(paths, n):
    m = min(n, len(paths))

    new_paths = dict()
    for i in range(m):
        new_paths[i] = paths[i]
    