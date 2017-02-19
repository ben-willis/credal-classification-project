from __future__ import division
import random, math

from data import data
from diagnostics import accuracy, mse, cross_validate, compare
from lossfns import zero_one, squared_diff,  absolute_diff

def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_class(M, class_id, class_val):
	return [row for row in M if row[class_id]==class_val]

def p_a_map(M, col_id, col_values):
	M_t = transpose(M)
	vals = M_t[col_id]
	return [(vals.count(a)+(1*(1/len(col_values))))/(len(vals) + 1) for a in col_values]

def p_ai_given_c_map(M, a_id, c_id, a_values, c_values):
	probs = []
	for c in c_values:
		M_filtered = filter_by_class(M, c_id, c)
		try:
			vals = transpose(M_filtered)[a_id]
		except IndexError as e:
			probs.append([(1*(1/len(a_values))*(1/len(c_values)))/(1*(1/len(c_values))) for a in a_values])
		else:
			probs.append([(vals.count(a)+(1*(1/len(a_values))*(1/len(c_values))))/(len(vals) + (1*(1/len(c_values)))) for a in a_values])
	return probs

def train_classifier(data, values, a_ids, c_id):
	p_cs = p_a_map(data, c_id, values[c_id])
	p_ai_given_cs = [p_ai_given_c_map(data, a_id, c_id, values[a_id], values[c_id]) for a_id in a_ids]
	def trained_classifier(obj):
		p_c_given_ais = [0] * len(values[c_id])
		for c in values[c_id]:
			p_c_given_ais[c] = p_cs[c]
			for a_id in a_ids:
				p_c_given_ais[c] = p_c_given_ais[c] * p_ai_given_cs[a_id][c][obj[a_id]]
		normalizing_factor = sum(p_c_given_ais)
		p_c_given_ais = [prob/normalizing_factor for prob in p_c_given_ais]
		return (zero_one(p_c_given_ais), squared_diff(p_c_given_ais), absolute_diff(p_c_given_ais))
	return trained_classifier

# res = []
# se = 1000
# res.append(cross_validate(data, 24, train_classifier, mse, 10))
# while(se/math.sqrt(len(res)) > 0.005):
# 	res.append(cross_validate(data, 24, train_classifier, mse, 10))
# 	mean = sum(res)/len(res)
# 	se = math.sqrt( (1/(len(res)-1)) * sum([(x - mean)**2 for x in res]) )
# print mean

test = cross_validate(data, 24, train_classifier, compare, 10)

for row in test:
	print row