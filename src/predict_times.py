import numpy as np
import pandas as pd

from data_IO import read_input
from tools import create_incoming_roads_count, create_distance_between_nodes, create_paths_as_nodes, create_incoming_nodes

class ExpectedTimes():

    def __init__(self, df, paths):

        self.incoming_roads_count = create_incoming_roads_count(df)
        self.incoming_nodes = create_incoming_nodes(df)
        self.distance_between_nodes = create_distance_between_nodes(df)
        self.paths_as_nodes = create_paths_as_nodes(df, paths)
        self.df = df

    def to_node(self, node):
        """For a given node, we return a dictionary which gives the expected times at which the cars will reach the node, 
        and the direction from which the cars are coming.
        """
        # we intialize the dict
        sol = dict()
        for from_node in self.incoming_nodes[node]:
            sol[from_node] = list()

        for car_id in self.paths_as_nodes.keys():
            # DO THiNGS

if __name__ == '__main__':
    file_dir = './data/hashcode.in'
    df, paths, time_simulation, bonus = read_input(file_dir)

    times_predictor = ExpectedTimes(df, paths)
