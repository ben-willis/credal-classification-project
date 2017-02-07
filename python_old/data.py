import os
import pandas as pd

# Read the CSV file
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/automobile.csv'))

#Discretize continous attributes
for column in list(df):
	if (df[column].dtype == 'float64' or df[column].dtype == 'int64'):
		df[column] = pd.cut(df[column], 4)
	df[column] = df[column].astype('category')

# Randomly sort the data
df = df.sample(frac=1).reset_index(drop=True)

# Remove objects with missing attributes
df = df.dropna()