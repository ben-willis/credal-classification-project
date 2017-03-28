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

unclean_data = import_data('../data/automobile_discretized.csv')
unclean_data = remove_column(unclean_data, 0)

# for j in range(len(data)-1, -1, -1):
# 	if data[j][-1] == 0:
# 		data = remove_row(data, j)
# 	else:
# 		data[j][-1] = data[j][-1]-1

reduced_data = transpose(unclean_data)
reduced_data = remove_rows_with_missing_values(reduced_data)
reduced_data = transpose(reduced_data)

clean_data = remove_rows_with_missing_values(unclean_data)