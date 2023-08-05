from clustpipeline import runclust
import pandas as pd
import numpy as np


Xr = pd.read_csv('../ExampleData/2_Preprocessed/Data/X0', index_col=0, sep='\t', header=0)

r = runclust([Xr])

print(Xr.shape)

