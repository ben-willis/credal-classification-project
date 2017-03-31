from __future__ import division
import random, math

from diagnostics import accuracy, mse, unclassified, cross_validate, compare
from lossfns import zero_one, squared_diff,  absolute_diff, custom

def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_row(M, row_id, row_val):
	return [row for row in M if row[row_id]==row_val]

def p_c_estimates(M, col_id, col_values, s):
	M_t = transpose(M)
	t_c = 1/len(col_values)
	vals = M_t[col_id]
	return [(vals.count(a)+(s*t_c))/(len(vals) + s) for a in col_values]

def p_ai_given_c_estimates(M, a_id, c_id, a_values, c_values, s):
	probs = []
	t_c = 1/len(c_values)
	t_a = 1/(len(a_values) * len(c_values))
	for c in c_values:
		M_filtered = filter_by_row(M, c_id, c)
		try:
			vals = transpose(M_filtered)[a_id]
		except IndexError as e:
			vals = []
		probs.append([(vals.count(a)+(s*t_c*t_a))/(len(vals) + (s*t_c)) for a in a_values])
	return probs

def train_classifier(data, values, a_ids, c_id, s):
	p_cs = p_c_estimates(data, c_id, values[c_id], s)
	p_ai_given_cs = [p_ai_given_c_estimates(data, a_id, c_id, values[a_id], values[c_id], s) for a_id in a_ids]
	def trained_classifier(obj):
		p_c_given_ais = [0] * len(values[c_id])
		for c in values[c_id]:
			p_c_given_ais[c] = p_cs[c]
			for a_id in a_ids:
				p_c_given_ais[c] = p_c_given_ais[c] * p_ai_given_cs[a_id][c][obj[a_id]]
		normalizing_factor = sum(p_c_given_ais)
		p_c_given_ais = [prob/normalizing_factor for prob in p_c_given_ais]
		return custom(p_c_given_ais)
	return trained_classifier
