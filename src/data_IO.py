import pandas as pd
from collections import Counter

def read_input(file_dir):

    my_file = open(file_dir, "r")

    info_line = [int(x) for x in my_file.readline().strip().split()]

    time_simulation = info_line[0]
    n_edges = info_line[2]
    n_paths = info_line[3]
    bonus = info_line[4]

    edges = list()
    for _ in range(n_edges): 
        line = my_file.readline().strip().split()
        edges.append(line)

    df_edges = pd.DataFrame(data=edges, columns=['from', 'to', 'name', 'lenght'])
    df_edges['from'] = pd.to_numeric(df_edges['from'])
    df_edges['to'] = pd.to_numeric(df_edges['to'])
    df_edges['lenght'] = pd.to_numeric(df_edges['lenght'])

    paths_dict = dict()
    next_road_dict = dict()

    for id_car in range(n_paths): 
        line = my_file.readline().strip().split()
        paths_dict[id_car] = line[1:]
        
        line_helper = line[1:] + ['end']

        path_next_road = dict()
        for i in range(len(line)-1): 
            path_next_road[line_helper[i]] = line_helper[i+1]

        next_road_dict[id_car] = path_next_road

    my_file.close


    df = add_edge_count_col(paths_dict, df_edges)

    # consider only used edges
    df = df.loc[df['count'] > 0]
    df['count'] = df['count'].astype(int)

    df = df.sort_values(by=['to', 'from'])


    return df, paths_dict, next_road_dict, time_simulation, bonus


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
    
def write_output(our_schedule):

    file = open('submission.txt', "a")

    for row in our_schedule:
        file.write(str(row) + '\n')


if __name__ == '__main__':
    file_dir = './data/hashcode.in'
    read_input(file_dir)
    



    
