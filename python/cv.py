from __future__ import division

import pandas as pd

# Assigns a groups from 1-k to each object in the dataframe (df). Groups are roughly of equal size.
def assign_groups(df, k):
	df['cv-group'] = pd.Series([i%k for i in range(len(df))], index=df.index)
	return df

# Select objects from df in group i
def select_objects(df, i):
	return df[df['cv-group'] == i]

# Select objects from df not in group i
def select_others(df, i):
	return df[df['cv-group'] != i]

def cross_validate(df, train_classifier, k):
	df = assign_groups(df, k)

	results = []
	# for each group
	for i in range(k):
		# determine test and train sets
		test = select_objects(df, i)
		train = select_others(df, i)

		# determine attributes used by classifier
		columns = list(df)
		columns.remove('Symboling')
		columns.remove('cv-group')

		# train the classifier
		classifier = train_classifier(train, 'Symboling', columns)
		
		# for each object classify and determine correctnes
		for index, row in test.iterrows():
			if row['Symboling'] == classifier(row):
				results.append(1)
			else:
				results.append(0)

	# return accuracy
	return sum(results)/len(results)