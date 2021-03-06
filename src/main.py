import pandas as pd
from multiprocessing import Pool
import time
import numpy as np

from data_IO import read_input
from tools import add_edge_count_col, create_random_node_order, less_paths, evaluate_simulation
from genetic_alg import times_crossover, order_crossover


def first_part(input_file_dir):

    df_edges, paths = read_input(input_file_dir)

    df_edges = add_edge_count_col(paths, df_edges)

    # consider only used edges
    df = df_edges.loc[df_edges['count'] > 0]

    print(str(len(df_edges)-len(df)) + ' edges are never used and therefore are not considered.')
    print('We are left with ' + str(len(df)) + ' edges')

    df['count'] = df['count'].astype(int)

    return df

if __name__ == '__main__':

    samples_gen0 = 8

    file_dir = './data/hashcode.in'

    df = first_part(file_dir)

    gen0_orders = list()
    print('a')
    for _ in range(samples_gen0):
        gen0_orders.append(create_random_node_order(df))
    gen0_times = list()

    times_min = [1]*len(df)
    times_max = list(df['count'].values)
    gen0_times.append(times_min)
    gen0_times.append(times_max)

    for _ in range(samples_gen0-2):
        gen0_times.append(times_crossover(times_min, times_max))
    

    gen0_scores = list()
    for i in range(samples_gen0):
        gen0_scores.append(evaluate_simulation(gen0_times[i], gen0_orders[i]))

    print(gen0_scores)
    ### first crossover 
    # gen_1 = list()
    # gen_1_scores = list()
    # for i in range(samples_gen0):
    #     for j in range(i+1,samples_gen0):
    #         print(i, j)


    #order_c = order_crossover(order_a, order_b)


    