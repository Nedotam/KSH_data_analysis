import sys
print(sys.executable)  # This should point to the virtual environment python
print(sys.path)        # This should include your virtual environment's site-packages

import pandas as pd
import numpy as np
import scipy
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from src.utils import read_csv_file, utils


path = '../data/raw/'
file = 'dummy.csv'
df=read_csv_file(path, file,'latin-1',';',)
print(df)
print('geci')
