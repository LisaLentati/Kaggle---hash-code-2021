import numpy as np


class Simulation:
    def __init__(self, simulation_time, used_edges, edge_lenght, bonus, paths_as_list, paths_as_next_road): 

        self.simulation_time = simulation_time   # int value
        self.used_edges = used_edges # list of roads
        self.edge_lenght = edge_lenght # dict, each edge is associated with their length
        self.bonus = bonus # number of points for each car that reaches the end

        self.paths_list = paths_as_list # a dict of lists, the paths of the cars 
        self.paths_next_road = paths_as_next_road # a dict of dicts, the paths of the cars

        self.initial_state_cars_at_nodes = self.create_initial_state_nodes()
        self.initial_state_cars_in_edges = self.create_initial_state_edges()


    def create_initial_state_nodes():
        cars_at_nodes = dict()
        for edge in self.used_edges:
            cars_at_nodes[edge] = list()

        for car_id in range(len(paths)):
            path = paths[car_id]
            first_road = path[0]
            cars_at_nodes[first_road].append(car_id)

        return cars_at_nodes

    def create_initial_state_edges(): 
        cars_in_edges = dict()
        for edge in self.used_edges:
            cars_in_edges[edge] = dict()
        
        return cars_in_edges


    def evaluate_schedule(schedule_df):

        score=0

        traffic_lights = self.initial_state_cars_at_nodes
        roads = self.initial_state_cars_in_edges

        for t in range(self.simulation_time): 
            update_state(traffic_lights, roads)
            # RIINIZIARE DA QUA
        return score    


    # def update_state():
    #     self.cars_at_nodes
    #     self.cars_in_edges

    #     for road in self.used_edges:
    #         if cars_at_nodes[road]:   # i.e. if there is a car waiting in that road
    #             crossing_car = cars_at_nodes[road].pop(0)
    #             next_road = paths[crossing_car][road]

    #             if next_road == 'end':
    #                 # give bonus points



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

        break
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

        if offset < x <= offset+green_time: 
            return True
        else:
            return False

    return green_light_fun
    



if __name__ == '__main__':
    from main import create_gen0
    from data_IO import read_input

    file_dir = './data/hashcode.in'
    df, next_road_dict, time_simulation, bonus = read_input(file_dir)
    
    samples_gen0 = 3
    gen_0 = create_gen0(df, samples_gen0)    
    schedule_df = gen_0[2]  # I choose the 3rd schedule to do the simulation on it

    simulation = Simulation(time_simulation, df['name'].values, df['lenght'].values, bonus, next_road_dict)



    green_light_functions = create_traffic_light_timetable(s)

    b=green_light_functions['g-a']
    print(b)
    for i in range(100):
        print(b(i))