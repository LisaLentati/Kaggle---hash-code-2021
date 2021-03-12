import numpy as np
import pandas as pd


class Simulation:
    def __init__(self, simulation_time, used_edges, edge_lenght_df, bonus, first_road, paths_as_next_road): 

        self.simulation_time = simulation_time   # int value
        self.used_edges = used_edges # list of roads
        self.edge_lenght = self.create_edge_lenght_dict(edge_lenght_df) # dict, each edge is associated with their length
        self.edge_lenght['end'] = -1
        self.bonus = bonus # number of points for each car that reaches the end

        self.paths_next_road = paths_as_next_road # a dict of dicts, the paths of the cars
        self.initial_state_df = self.create_initial_state(first_road)
        self.green_lights = None
      
    def create_initial_state(self, first_road):
        df = pd.DataFrame(data=first_road, columns=['car_id', 'road'])
        df = df.sort_values(by='car_id')
        df['node_pos'] = df.groupby(by='road').transform(lambda x: pd.Series(range(len(x))))
        df['road_pos'] = np.nan

        return df

    def create_edge_lenght_dict(self, edge_lenght_df):
        my_dict = dict()
        for row in edge_lenght_df.values:
            my_dict[row[0]] = row[1]

        return my_dict

    def evaluate_schedule(self, schedule_df):

    
        self.green_lights = create_traffic_light_functions(schedule_df)

        df = self.initial_state_df
        for t in range(self.simulation_time): 
            self.update_state(df, t)

        mask = df['road'] == 'end'

        score = sum(mask)*self.bonus +  (-1)*sum(df.loc[mask,'road_pos'])
        return score    

    def update_state(self, df, time):

        df['is_green'] = df['road'].apply(lambda x: self.green_lights[x](time))

        # ALL CARS IN THE ROADS MOVE BY ONE
        df['road_pos'] -= 1
        mask_new_cars_at_node = df['road_pos']==-1


        # UPDATE FOR THE CARS THAT ARE CROSSING A TRAFFIC LIGHT
        mask_cars_crossing = (df['node_pos'] == 0) & df['is_green']
        df.loc[mask_cars_crossing, 'road'] = df.loc[mask_cars_crossing, ['car_id', 'road']].apply(lambda x: self.paths_next_road[x['car_id']][x['road']], axis=1)
        df.loc[mask_cars_crossing, 'node_pos'] = np.nan
        df.loc[mask_cars_crossing, 'road_pos'] = df.loc[mask_cars_crossing, 'road'].apply(lambda x: self.edge_lenght[x])
        # UPDATE NODE POSITONS FOR CARS THAT ARE AT A GREEN TRAFFIC LIGHT
        df.loc[df['is_green'], 'node_pos'] -= 1

        # WE TAKE AWAY THE ROAD POSITION FOR THE CARS THAT FINISHED TRAVELLING ON THE ROAD 
        df.loc[mask_new_cars_at_node, 'road_pos'] = np.nan

        # WE ASSIGN THE RIGHT NODE POSITION FOR THE CARS THAT FINISHED TRAVELLING ON THE ROAD. 
        df['at_node'] = df['node_pos'].notnull()
        node_pos_for_arriving_cars = dict(df.groupby(by='road')['at_node'].sum())
        df.loc[mask_new_cars_at_node, 'node_pos'] = df.loc[mask_new_cars_at_node, 'road'].apply(lambda x: node_pos_for_arriving_cars[x])
    
        return 
    

def create_traffic_light_functions(schedule_times):
    
    green_light = dict()

    for _, group in schedule_times.groupby(by='to'):
        cycle_length = group['time'].sum()
        group = group.sort_values(by='order')

        offset = 0

        for row in group.values:
            _, road_name, t, _ = row 
            
            green_light[road_name] = create_green_light_func(offset, t, cycle_length)
            offset = offset + t
        green_light['end'] = always_green
        
    return green_light


def create_green_light_func(offset, green_time, cycle): 
    """
    Args:
        offset (int): number of seconds before the light turns green the first time
        green_time (int): number of seconds the light remains green
        cycle (int): length of the cycle
        time (int): the time  for which we want to check if the traffic light is green

    Returns: a function which True if the light is green, False if the light is red.
    """
    def green_light_fun(time): 
        x = np.mod(time, cycle)

        if offset <= x < offset+green_time: 
            return True
        else:
            return False

    return green_light_fun


def always_green(time):
    return True
    



if __name__ == '__main__':
    from main import create_gen0
    from data_IO import read_input
    from collections import Counter
    import time

    x0 = time.time()
    file_dir = './data/hashcode.in'
    df, first_road, next_road_dict, time_simulation, bonus = read_input(file_dir)
    simulation = Simulation(time_simulation, df['name'].values, df[['name', 'lenght']], bonus, first_road, next_road_dict)
    x1 = time.time()
    print(np.round(x1-x0))

    samples_gen0 = 3
    gen_0 = create_gen0(df, samples_gen0)    
    schedule_df = gen_0[2]  # I choose the 3rd schedule to do the simulation on it
    x2 = time.time()
    print(np.round(x2-x1))

    simulation.evaluate_schedule(schedule_df)
    x3 = time.time()
    print(np.round(x3-x2))