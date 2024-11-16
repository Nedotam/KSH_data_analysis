import pandas as pd
import numpy as np
import scipy
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from src.utils import utils

path = '../data/raw/'
file = 'dummy.csv'
df=utils.read_csv_file()
if df is not None:
    print(df)
if df is None:
    print(':(')