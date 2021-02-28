import numpy as np

def schedule(dict_paths, used_edges, nodes_to_edges, num_nodes):

    edge_array = np.array(used_edges)

    tally = {}

    for edge in used_edges:
       tally[tuple(edge)]= 0

    for key in dict_paths.keys():
        for edge in dict_paths[key]:
            tally[edge] += 1
        

    schedule = {}

    for i in range(num_nodes):

        index_list = list(np.where(edge_array.T[1] == i)[0])
        your_edges = edge_array[index_list]

        if len(list(your_edges)) > 0 :
            times = find_schedule(tally, your_edges)
            schedule[i] = [your_edges, times]
        
    return schedule


def find_schedule(tally, your_edges):

    times = []
    for edge in your_edges:
        times.append(tally[tuple(edge)])

    times = np.array(times)
    ratios = times / np.sum(times)
    times = method_1(ratios)
    
    return times

def method_1(ratios):
    cycle_length = len(ratios)*2

    approx_val = [i*cycle_length for i in ratios]
    int_val = [int(np.round(i)) for i in approx_val]
    int_val_fix = [i if i>0 else 1 for i in int_val]  # zeros become ones
    return int_val_fix


if __name__ == '__main__':
    a = [0.2, 0.111, 0.3, 0.199, 0.1, 0.095, 0.005]

    method_1(a)