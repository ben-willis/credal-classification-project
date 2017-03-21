import os, csv

from collections import Counter

def import_data(path):
	data = []
	with open(os.path.join(os.path.dirname(__file__), path)) as datafile:
		next(datafile, None)
		for row in csv.reader(datafile):
			data.append([int(value) for value in row])
	return data

def transpose(M):
	return [list(i) for i in zip(*M)]

def remove_row(M, j):
	return M[:j] + M[j+1:]

def remove_column(M, i):
	M_t = transpose(M)
	M_t = remove_row(M_t, i)
	return transpose(M_t)

def remove_rows_with_missing_values(M):
	for j in range(len(M)-1, -1, -1):
		if -1 in M[j]:
			M = remove_row(M, j)
	return M

data = import_data('../data/automobile_discretized.csv')
data = remove_column(data, 0)

data_cleaned = remove_rows_with_missing_values(data)