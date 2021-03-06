import pandas as pd
from multiprocessing import Pool
import time
import numpy as np
import pandas as pd
from functools import partial

from tools import create_random_order
from genetic_alg import times_crossover, order_crossover1


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

    rng = np.random.default_rng()
    for _ in range(samples-2):
        times_min = df_skeleton.copy()
        times_min['time'] = [rng.choice(np.arange(0, 2), p=[0.2,0.8]) for _ in range(len(times_min))]
        new_schedule = df_skeleton.copy()
        new_schedule['time'] = times_crossover(times_min['time'], times_max['time'])
        create_random_order(new_schedule)
        gen0_schedules.append(new_schedule)

    return gen0_schedules



if __name__ == '__main__':
    from data_IO import read_input
    from simulation import create_edge_lenght_dict, evaluate_schedule
    import time
    import os

    file_dir = './data/hashcode.in'
    df, first_road, next_road_dict, time_simulation, bonus = read_input(file_dir)
    df_skeleton = df[['to', 'name']]

    edge_lenght = create_edge_lenght_dict(df[['name', 'lenght']])
    edge_lenght['end'] = -1

    times_min = df_skeleton.copy()
    times_min['time'] = [1]*len(df)
    times_max = df_skeleton.copy()
    times_max['time'] = df['count'].values

    create_random_order(times_min)
    create_random_order(times_max)

    eval_sched = partial(evaluate_schedule, first_road=first_road, bonus=bonus, simulation_time=time_simulation, paths_next_road=next_road_dict, edge_lenght=edge_lenght)

    results_gen_0 = list()
    gen_0 = [times_min, times_max]

    p = Pool() 

    results_gen_0 = p.map(eval_sched, gen_0)
    p.close()
    p.join()


    df_directories = os.listdir("./trial1/")
    for j in range(10):
        mask = list(map(lambda x: x[:4]=='7_' + str(j) + '_', df_directories) )
        
        dir_file = np.array(df_directories)[mask][0]
        score = int(float(dir_file[4:-4]))
        gen_0.append(pd.read_csv("./trial1/" + dir_file))
        results_gen_0.append(score)

    for j in range(10,14):
        mask = list(map(lambda x: x[:4]=='7_' + str(j), df_directories))
        dir_file = np.array(df_directories)[mask][0]
        score = int(float(dir_file[5:-4]))
        gen_0.append(pd.read_csv("./trial1/" + dir_file))
        results_gen_0.append(score)


    generations_info = [(8, 16, 50), (9, 10, 20), (10, 10, 20)]

    for gen_info in generations_info:
        idx, to_keep, to_create = gen_info
        print(idx)
        best_ids = sorted(range(len(results_gen_0)), key=lambda i: results_gen_0[i])[-to_keep:]

        all_combinations = list()
        for i in range(to_keep):
            for j in range(i+1,to_keep):
                all_combinations.append((best_ids[i],best_ids[j]))

        choosen_kids_id = np.random.choice(range(len(all_combinations)), size=to_create, replace=False)
        choosen_kids = [all_combinations[i] for i in choosen_kids_id]
        print(choosen_kids)

        gen_1 = list()
        for i,j in choosen_kids:
            new_schedule = df_skeleton.copy()
            new_schedule['time'] = times_crossover(gen_0[i]['time'], gen_0[j]['time'])
            new_schedule['order'] = order_crossover1(gen_0[i], gen_0[j])
            gen_1.append(new_schedule)

        p = Pool() 

        results_gen_1 = p.map(eval_sched, gen_1)
        p.close()
        p.join()

        print(results_gen_1)

        for i in range(len(gen_1)):
            dff = gen_1[i]
            name = str(idx) + '_' + str(i) + '_' + str(results_gen_1[i]) + '.csv'
            dff.to_csv(name, index=False)
    

        for idx in best_ids:
            gen_1.append(gen_0[idx])
            results_gen_1.append(results_gen_0[idx])

        gen_0 = gen_1
        results_gen_0 = results_gen_1



