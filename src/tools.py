import numpy as np
import pandas as pd




def create_random_order(df):
    """Takes a dataframe and adds to it a column called 'order'.    
    """
    
    rng = np.random.default_rng()
    df['order'] = df.groupby(by='to').apply(lambda x: pd.Series(rng.permutation(np.arange(len(x))))).values
    return


    