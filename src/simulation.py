import numpy as np


class Simulation:
    def __init__(self, simulation_time, used_edges, edge_lenght, bonus, paths): 

        self.simulation_time = simulation_time   # int value
        self.used_edges = used_edges # list of roads
        self.edge_lenght = edge_lenght # dict, each edge is associated with their length
        self.bonus = bonus # number of points for each car that reaches the end

        self.paths = paths # a dict of the paths of the cars

        self.cars_at_nodes = self.create_initial_state_nodes()
        self.cars_in_edges = self.create_initial_state_edges()


    def create_initial_state_nodes():
        cars_at_nodes = dict()
        for edge in self.used_edges:
            cars_at_nodes[edge] = list()

        for car_id  in range(len(paths)):
            path = paths[car_id]
            for road in path:
                cars_at_nodes[road].append(car_id)

        return cars_at_nodes

    def create_initial_state_edges(): 
        cars_in_edges = dict()
        for edge in self.used_edges:
            cars_in_edges[edge] = dict()
        
        return cars_in_edges

def create_traffic_light_timetable(schedule_times, schedule_order):
    # TODO
    edges_green_light = dict()

    for node in schedule_order.keys():
        order = schedule_order[node]

        offset = 0
        for 

        edges_green_light[edge] = create_green_light_func()
    return timetable


def create_green_light_func(offset, green_time, cycle): 
    """
    Args:
        offset (int): number of seconds before the light turns green the first time
        green_time (int): number of seconds the light remains green
        cycle (int): length of the cycle
        time (int): the time  for which we want to check if the traffic light is green

    Returns: a function which True if the light is green, False if the light is red.
    """
    def green_light(time): 
        x = np.mod(time, cycle)

        if offset < x <= offset+green_time: 
            return True
        else:
            return False

    return green_light
    



def evaluate_simulation(schedule_times, schedule_order, simulation_time, paths_list):

    score=0

    at_traffic_light = dict()

    #for t in range(simulation_time): 

    return score    


if __name__ == '__main__':
    cycle = 5
    offset = 1
    green  = 2



    for i in range(1, 13):
        print(green_light(offset,green, cycle, i))