import pandas as pd

def read_input(file_dir):

    my_file = open(file_dir, "r")

    info_line = [int(x) for x in my_file.readline().strip().split()]

    n_edges = info_line[2]
    n_paths = info_line[3]

    edges = list()
    for _ in range(n_edges): 
        line = my_file.readline().strip().split()
        edges.append(line)

    df_edges = pd.DataFrame(data=edges, columns=['from', 'to', 'name', 'lenght'])
    df_edges['from'] = pd.to_numeric(df_edges['from'])
    df_edges['to'] = pd.to_numeric(df_edges['to'])
    df_edges['lenght'] = pd.to_numeric(df_edges['lenght'])

    paths = dict()

    for i in range(n_paths): 
        line = my_file.readline().strip().split()
        paths[i] = line[1:]
    
    my_file.close
    return df_edges, paths



def write_output(our_schedule):

    file = open('submission.txt', "a")

    for row in our_schedule:
        file.write(str(row) + '\n')


if __name__ == '__main__':
    file_dir = 'hashcode.in'
    edges, paths = read_data(file_dir)
    



    
