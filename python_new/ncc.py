from __future__ import division
import random

# import numpy as np
# import matplotlib.pyplot as plt

from data import data
from diagnostics import cross_validate, single_accuracy, set_accuracy, indeterminate_output_size, determinacy


def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_row(M, row_id, row_val):
	return [row for row in M if row[row_id]==row_val]

def n_c(M, col_id, col_values):
	M_t = transpose(M)
	vals = M_t[col_id]
	return [vals.count(c) for c in col_values]

def n_ai_c(M, a_id, c_id, a_values, c_values):
	counts = []
	for c in c_values:
		M_filtered = filter_by_row(M, c_id, c)
		try:
			vals = transpose(M_filtered)[a_id]
		except IndexError as e:
			vals = []
		counts.append([vals.count(a) for a in a_values])
	return counts

def create_obj_function(data, values, a_ids, c_id):
	s = 2
	n_cs = n_c(data, c_id, values[c_id])
	n_ai_cs = [n_ai_c(data, a_id, c_id, values[a_id], values[c_id]) for a_id in a_ids]
	def obj_function(obj, c1, c2, x):
		res = ((n_cs[c2] + (s*x))/(n_cs[c1]+s-(s*x)))**(len(a_ids)-1)
		for a_id in a_ids:
			res = res * (n_ai_cs[a_id][c1][obj[a_id]])/(n_ai_cs[a_id][c2][obj[a_id]] + (s*x))
		return res
	return obj_function

def find_minimum(f):
	minimum = f(1)
	for i in range(100):
		value = f((i+1)/100)
		minimum = value if (value < minimum) else minimum
	return minimum

def train_classifier(data, values, a_ids, c_id):
	f = create_obj_function(data, values, a_ids, c_id)
	def trained_classifier(obj):
		dominated = []
		for c1 in values[c_id]:
			dominated.append(False)
			for c2 in values[c_id]:
				def obj_f(x):
					return f(obj, c2, c1, x)
				minimum = find_minimum(obj_f)
				if (minimum) > 1:
					dominated[-1] = True
					break;
		return [i for i in range(len(values[c_id])) if not dominated[i]]
	return trained_classifier



def get_classes(M, col_id):
	M_t = transpose(M)
	return list(set(M_t[col_id]))

while True:
	cross_validate(data, 24, train_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10)

	# x = np.arange(0.01,1,0.01)
	# axes = plt.gca()
	# axes.set_ylim([0,2])
	# plt.plot(x, f(x))
	# plt.show()