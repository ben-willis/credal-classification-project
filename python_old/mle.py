from __future__ import division
import pandas as pd

# Determine mle for P(c) for each class in c_column of df 
def p_c_mle(df, c_column):
	classes = df[c_column].cat.categories.tolist()
	relative_frequencies = [ len(df[df[c_column] == c].index) / len(df.index) for c in classes]
	return pd.Series(relative_frequencies, index=classes)

# Determine mle for P(a|c) for each class in c_column and attribute in a_column
def p_a_given_c_mle(df, a_column, c_column):
	classes = df[c_column].cat.categories.tolist()
	attribute_values = df[a_column].cat.categories.tolist()

	relative_frequencies = []
	for c in classes:
		x = df[df[c_column] == c][a_column]
		relative_frequencies.append([len(x[x == a].index) / len(x.index) for a in attribute_values])
	return pd.DataFrame(relative_frequencies, index=classes, columns=attribute_values)

# train the classifier
def train_classifier(df, c_column, a_columns):

	p_c = p_c_mle(df, c_column)

	p_a_given_c = dict()
	# for each attribute calculate mle for P(a|c)
	for a_column in a_columns:
		p_a_given_c[a_column] = p_a_given_c_mle(df, a_column, c_column)

	def classifier(obj):
		estimates = dict()

		for c in df[c_column].cat.categories.tolist():
			estimates[c] = p_c[c]
			for a_column in p_a_given_c:
				estimates[c] = estimates[c] * p_a_given_c[a_column][obj[a_column]][c]

		return max(estimates, key=lambda k: estimates[k])

	# return the trained classifier
	return classifier