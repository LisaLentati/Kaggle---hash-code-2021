import numpy as np
import pandas as pd
from collections import Counter


def count_used_edges(paths, df_edges):
    """Adds the column 'counts' to df_edges. Indicating how many times each edge 
    appears in paths (i.e. a car goes through the edge).
    """

    list_travelled_edges = list()
    for i in paths.keys():
        list_travelled_edges += paths[i]

    c = dict(Counter(list_travelled_edges))
    df_counts = pd.Series(c).reset_index(name='counts')
    df_counts = df_counts.rename(columns={'index': 'name'})

    df_edges = pd.merge(df_edges, df_counts, how='left', on='name')
        
    return df_edges

def create_schedule(df_edges):
    schedule_list = list()

    # take edges which are used
    df = df_edges.loc[~df_edges.counts.isna()]

    end_nodes = df['to'].unique()

    schedule_list.append(len(end_nodes))

    for end_node in end_nodes:
        schedule_list.append(end_node)
        small_df = df.loc[df.to == end_node]

        l = len(small_df)
        schedule_list.append(l)   

        node_counts = small_df['counts'].values
        node_streets = small_df['name'].values

        node_schedule = method_1(node_counts) 
        for i in range(l):
            row = node_streets[i] + ' ' + str(int(node_schedule[i]))
            schedule_list.append(row)
    
    return schedule_list


def method_1(counts):
    cycle_length = len(counts)*1.5

    m = sum(counts)
    ratios = counts/m

    approx_val = [i*cycle_length for i in ratios]
    int_val = [int(np.round(i)) for i in approx_val]
    int_val_fix = [i if i>0 else 1 for i in int_val]  # zeros become ones
    return int_val_fix


if __name__ == '__main__':
    import data_IO
    url = 'hashcode.in'
    df_edges, paths = data_IO.read_data(url)

    schedule(paths, df_edges)
    # a = [0.2, 0.111, 0.3, 0.199, 0.1, 0.095, 0.005]

    # method_1(a)