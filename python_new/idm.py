from __future__ import division
import random, math

from data import data_cleaned as data
from diagnostics import accuracy, mse, unclassified, cross_validate, compare, set_accuracy, single_accuracy, indeterminate_output_size, determinacy
from lossfns import zero_one, squared_diff,  absolute_diff, credal, upper, lower

def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_row(M, row_id, row_val):
	return [row for row in M if row[row_id]==row_val]

def p_c_estimates(M, col_id, col_values, s):
	M_t = transpose(M)
	vals = M_t[col_id]
	return [((vals.count(a))/(len(vals) + s), (vals.count(a)+s)/(len(vals) + s)) for a in col_values]

def p_ai_given_c_estimates(M, a_id, c_id, a_values, c_values, s):
	probs = []
	for c in c_values:
		M_filtered = filter_by_row(M, c_id, c)
		try:
			vals = transpose(M_filtered)[a_id]
		except IndexError as e:
			vals = []
		probs.append([((vals.count(a))/(len(vals) + s), (vals.count(a) + s)/(len(vals)+s))  for a in a_values])
	return probs

def train_classifier(data, values, a_ids, c_id, s):
	p_cs = p_c_estimates(data, c_id, values[c_id],s)
	p_ai_given_cs = [p_ai_given_c_estimates(data, a_id, c_id, values[a_id], values[c_id],s) for a_id in a_ids]
	def trained_classifier(obj):
		p_c_given_ais_lower = [0] * len(values[c_id])
		p_c_given_ais_upper = [0] * len(values[c_id])
		for c in values[c_id]:
			p_c_given_ais_lower[c] = p_cs[c][0]
			p_c_given_ais_upper[c] = p_cs[c][1]
			for a_id in a_ids:
				p_c_given_ais_lower[c] = p_c_given_ais_lower[c] * p_ai_given_cs[a_id][c][obj[a_id]][0]
				p_c_given_ais_upper[c] = p_c_given_ais_upper[c] * p_ai_given_cs[a_id][c][obj[a_id]][1]
		p_c_given_ais_intervals = zip(p_c_given_ais_lower, p_c_given_ais_upper)
		# print "-------"
		# for p_c_given_ais in p_c_given_ais_intervals:
		# 	c = p_c_given_ais_intervals.index(p_c_given_ais)
		# 	if obj[c_id] == c:
		# 		print str(c) + "*: [" + str(p_c_given_ais[0]) + ", " + str(p_c_given_ais[1]) + "]"
		# 	else:
		# 		print str(c) + " : [" + str(p_c_given_ais[0]) + ", " + str(p_c_given_ais[1]) + "]"
		return credal(p_c_given_ais_intervals)
	return trained_classifier