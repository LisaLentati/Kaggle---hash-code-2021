import numpy as np

def read_data(file_url):

    my_file = open(file_url, "r")

    info_line = [int(x) for x in my_file.readline().strip().split()]

    simulation_s = info_line[0]
    n_nodes = info_line[1]
    n_edges = info_line[2]
    n_paths = info_line[3]
    points = info_line[4]

    rue_to_nodes = dict()
    rue_lengths = dict()

    for _ in range(n_edges): 
        line = my_file.readline().strip().split()
        rue_to_nodes[line[2]] = [int(line[0]), int(line[1])]
        rue_lengths[line[2]] = int(line[3])

    nodes_to_rue = dict()
    for i in rue_to_nodes.keys():
        nodes_to_rue[tuple(rue_to_nodes[i])] = i

    paths = dict()
    paths_length = dict()
    edges_used = set()

    for i in range(n_paths): 
        line = my_file.readline().strip().split()
        the_path = line[1:]
        paths[i] = [tuple(rue_to_nodes[rue]) for rue in the_path]   

        paths_length[i] = np.sum(np.array([rue_lengths[rue] for rue in the_path])) 
        for rue in the_path:
            edges_used.add(tuple(rue_to_nodes[rue]))

    edges_used_list = [list(i) for i in list(edges_used)]
    my_file.close

    return rue_to_nodes, nodes_to_rue, rue_lengths, paths, n_nodes, edges_used_list, paths_length





if __name__ == '__main__':
    url = './data/a.txt'
    a, b, c, d, e, f, g = read_data(url)

    print(d)
    print(g)
    
