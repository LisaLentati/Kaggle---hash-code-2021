import numpy as np


class Simulation:
    def __init__(self, simulation_time, used_edges, edge_lenght_df, bonus, paths_as_list, paths_as_next_road): 

        self.simulation_time = simulation_time   # int value
        self.used_edges = used_edges # list of roads
        self.edge_lenght = self.create_edge_lenght_dict(edge_lenght_df) # dict, each edge is associated with their length
        self.bonus = bonus # number of points for each car that reaches the end

        self.paths_list = paths_as_list # a dict of lists, the paths of the cars 
        self.paths_next_road = paths_as_next_road # a dict of dicts, the paths of the cars

        self.initial_state_cars_at_nodes = self.create_initial_state_nodes()
        self.initial_state_cars_in_edges = self.create_initial_state_edges()


    def create_initial_state_nodes(self,):
        cars_at_nodes = dict()
        for edge in self.used_edges:
            cars_at_nodes[edge] = list()

        for car_id in range(len(self.paths_list)):
            path = self.paths_list[car_id]
            first_road = path[0]
            cars_at_nodes[first_road].append(car_id)

        return cars_at_nodes

    def create_initial_state_edges(self,): 
        cars_in_edges = dict()
        for edge in self.used_edges:
            cars_in_edges[edge] = dict()
        
        return cars_in_edges

    def create_edge_lenght_dict(self, edge_lenght_df):
        my_dict = dict()
        for row in edge_lenght_df.values:
            my_dict[row[0]] = row[1]

        return my_dict

    def evaluate_schedule(self, schedule_df):

        score=0
    
        green_light_times = create_traffic_light_functions(schedule_df)
        at_traffic_lights = self.initial_state_cars_at_nodes
        in_roads = self.initial_state_cars_in_edges
        
        for t in range(self.simulation_time): 
            points = self.update_state(at_traffic_lights, in_roads, green_light_times, t)
            score = score + points
            print(t, score)
        return score    

    def update_state(self, cars_at_nodes, cars_in_edges, is_green, time):
        points = 0

        for road in self.used_edges:
            # first we move all cars_in_edges by one
            for car in cars_in_edges[road].keys():
                cars_in_edges[road][car] -= 1

            if is_green[road](time):   # if the traffic light on the road is green in this particular time
                if cars_at_nodes[road]:  # if there is a car at the trafffic light that can pass
                    crossing_car = cars_at_nodes[road].pop(0) # we let the car pass 
                    next_road = self.paths_next_road[crossing_car][road] # we check the next road the car is taking

                    if next_road == 'end':  # if the car has reached the end
                        # give bonus points
                        points = points + self.bonus
                        points = points + (self.simulation_time - time)

                    else: # if the car has not reached the end
                        # we add it to the next road, with an indication of how many seconds the car will need 
                        # to go through the road
                        cars_in_edges[next_road][crossing_car] = self.edge_lenght[next_road]
                        


            # if a car has finished an edges it is moved to the cars_at_nodes traffic light
            for car in list(cars_in_edges[road].keys()):
                if cars_in_edges[road][car] == 0:
                    del cars_in_edges[road][car]
                    cars_at_nodes[road].append(car)

        return points


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
    df, paths_dict, next_road_dict, time_simulation, bonus = read_input(file_dir)
    
    samples_gen0 = 3
    gen_0 = create_gen0(df, samples_gen0)    
    schedule_df = gen_0[2]  # I choose the 3rd schedule to do the simulation on it

    simulation = Simulation(time_simulation, df['name'].values, df[['name', 'lenght']], bonus, paths_dict, next_road_dict)

    simulation.evaluate_schedule(schedule_df)