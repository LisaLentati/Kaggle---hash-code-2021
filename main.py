from src import read_data, schedule
import pandas as pd


def output(our_schedule, nodes_to_rue, num_nodes, val):

    file = open('output' + str(val) + '.txt', "a")

    file.write(str(len(list(our_schedule.keys()))) + '\n')

    for key in our_schedule.keys():
        file.write(str(key) + '\n')

        edges = our_schedule[key][0]
        times = our_schedule[key][1]

        file.write(str(len(edges)) + '\n')
        for i in reversed(range(len(edges))):
            file.write(str(nodes_to_rue[tuple(edges[i])]) + ' ' + str(times[i]) + '\n')


def choose_paths(paths, used_edges, paths_length, rue_to_nodes):
    sorted_lengths = sorted(list(paths_length.values()))

    end_ind = int(0.99 * len(sorted_lengths))
    cut_off = sorted_lengths[end_ind]
    
    new_edges_used = set()
    new_paths = {}
    for path in paths.keys():
        if paths_length[path] <= cut_off:
            new_paths[path] = paths[path]
            
            for edge in new_paths[path]:
                new_edges_used.add(tuple(edge))

    new_edges_used_list = [list(i) for i in list(new_edges_used)]

            
    return new_paths, new_edges_used_list



if __name__ == '__main__':
    for val in ['a', 'b', 'c', 'd', 'e', 'f']:
        url = './data/' + str(val) + '.txt'
        rue_to_nodes, nodes_to_rue, rue_lengths, paths, num_nodes, used_edges, paths_length = read_data.read_data(url)

        new_paths, new_used_edges = choose_paths(paths, used_edges, paths_length, rue_to_nodes)
        
        our_schedule = schedule.schedule(new_paths, new_used_edges, nodes_to_rue, num_nodes)

        output(our_schedule, nodes_to_rue, num_nodes, val)
