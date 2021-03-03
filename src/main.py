from data_IO import read_input
import pandas as pd




if __name__ == '__main__':
    url = './data/hashcode.in'
    df_edges, paths = read_input(url)
    print(df_edges)
    