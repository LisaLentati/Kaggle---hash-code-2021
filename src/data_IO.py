import pandas as pd
from tools import add_edge_count_col

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

    paths = dict()

    for id_car in range(n_paths): 
        line = my_file.readline().strip().split()

        paths[id_car] = line[1:]
        
    my_file.close


    df = add_edge_count_col(paths, df_edges)

    # consider only used edges
    df = df.loc[df['count'] > 0]
    df['count'] = df['count'].astype(int)

    df = df.sort_values(by=['to', 'from'])

    return df, paths, time_simulation, bonus

    
def write_output(our_schedule):

    file = open('submission.txt', "a")

    for row in our_schedule:
        file.write(str(row) + '\n')


if __name__ == '__main__':
    file_dir = './data/hashcode.in'
    read_input(file_dir)
    



    
