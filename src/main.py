import pandas as pd
from multiprocessing import Pool
import time
import numpy as np

from tools import create_random_order
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
    from data_IO import read_input
    import time

    x0 = time.time()
    file_dir = './data/hashcode.in'
    df, first_road, next_road_dict, time_simulation, bonus = read_input(file_dir)
    simulation = Simulation(time_simulation, df['name'].values, df[['name', 'lenght']], bonus, first_road, next_road_dict)

    samples_gen0 = 40
    gen_0 = create_gen0(df, samples_gen0)    
    schedule_df = gen_0[2]  # I choose the 3rd schedule to do the simulation on it
    x2 = time.time()
    print(np.round(x2-x1))

    simulation.evaluate_schedule(schedule_df)
    x3 = time.time()
    print(np.round(x3-x2))
    samples_gen0 = 8


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


    