import numpy as np
import pandas as pd

def times_crossover(times_A, times_B): 
    """ASSUMPTION: times_A, times_B are pd.Series
    """
    rng = np.random.default_rng()

    times_min = list(map(lambda x, y: min(x,y), list(times_A), list(times_B)))
    times_max = list(map(lambda x, y: max(x,y), list(times_A), list(times_B)))

    times_AB = map(lambda m, M: rng.choice(np.arange(m, M+1)), times_min, times_max)

    return list(times_AB)

def order_crossover(order_A, order_B):
    """ASSUMPTION: the schedules order_A and order_B have the same keys. 
    For each node i, order_A[i] and order_B[i] is a list containing the same edges.
    """
    rng = np.random.default_rng()
    order_AB = dict()
    for node in order_A.keys():
        order_AB[node] = order_crossover_node(order_A[node], order_B[node], rng)
        
    return order_AB

def order_crossover1(order_A, order_B):
    """ASSUMPTION: order_A and order_B are dataframes.
    """
    rng = np.random.default_rng()
    df = pd.DataFrame({'to': order_A['to'].values, 'order_a':order_A['order'].values, 
                       'order_b': order_B['order'].values})

    df['order'] = df.groupby(by='to').apply(lambda x: order_crossover_node1(x['order_a'], x['order_b'], rng)).values
        
    return df[ 'order'].values

def order_crossover_node1(order_A, order_B, rng):
    """
    order_A and order_B are columns of a dataframe
    """

    l_0 = int(np.floor(len(order_A)/2))
    i = rng.choice(np.arange(l_0+1))

    list_A = list(order_A)
    list_B = list(order_B)
    list_AB = list_A[i: i+l_0+1] 

    new_list = list_B.copy()
    for edge in list_AB:
        try:
            new_list.remove(edge)
        except:
            print("EXCEPT")
            print(edge)
            print(new_list)
            print(order_A, order_B)  
            break  
    
    return pd.Series(list_AB + new_list)

def order_crossover_node(list_A, list_B, rng):

    l_0 = int(np.floor(len(list_A)/2))
    i = rng.choice(np.arange(l_0+1))

    list_AB = list_A[i: i+l_0+1] 

    new_list = list_B.copy()
    for edge in list_AB:
        new_list.remove(edge)    
    
    return list_AB + new_list


if __name__ == '__main__':
    a = ['a', 'b', 'c', 'd', 'e', 'f' ]
    b = ['d', 'a', 'c', 'f', 'e', 'b']

    c = order_crossover_node(a,b, np.random.default_rng())
    print(c)
