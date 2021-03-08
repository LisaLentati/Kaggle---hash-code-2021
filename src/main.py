import pandas as pd
from multiprocessing import Pool
import time
import numpy as np

from data_IO import read_input
from tools import add_edge_count_col, create_random_order, less_paths
from genetic_alg import times_crossover, order_crossover


def create_gen0(df, samples): 
    df_skeleton = df[['to', 'name']]

    gen0_schedules = list()

    times_min = df_skeleton.copy()
    times_min['time'] = [1]*len(df)
    times_max = df_skeleton.copy()
    times_max['time'] = df['count'].values

    create_random_order(times_min)
    create_random_order(times_max)
    gen0_schedules.append(times_min)
    gen0_schedules.append(times_max)

    for _ in range(samples-2):
        new_schedule = df_skeleton.copy()
        new_schedule['time'] = times_crossover(times_min['time'], times_max['time'])
        create_random_order(new_schedule)
        gen0_schedules.append(new_schedule)

    return gen0_schedules



if __name__ == '__main__':

    samples_gen0 = 8

    file_dir = './data/hashcode.in'

    df, _, _, _, _ = read_input(file_dir)

    gen_0 = create_gen0(df, samples_gen0)
    print(gen_0[4].head(20))
    

    # gen0_scores = list()
    # for i in range(samples_gen0):
    #     gen0_scores.append(evaluate_simulation(gen0_times[i], gen0_orders[i]))

    # print(gen0_scores)
    ### first crossover 
    # gen_1 = list()
    # gen_1_scores = list()
    # for i in range(samples_gen0):
    #     for j in range(i+1,samples_gen0):
    #         print(i, j)


    #order_c = order_crossover(order_a, order_b)


    