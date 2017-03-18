from __future__ import division
import random, math

from data import data
from diagnostics import accuracy, mse, unclassified, cross_validate, compare
from lossfns import zero_one

def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_class(M, class_id, class_val):
	return [row for row in M if row[class_id]==class_val]

def p_a_mle(M, col_id, col_values):
	M_t = transpose(M)
	vals = M_t[col_id]
	return [(vals.count(a)/len(vals)) for a in col_values]

def p_ai_given_c_mle(M, a_id, c_id, a_values, c_values):
	probs = []
	for c in c_values:
		M_filtered = filter_by_class(M, c_id, c)
		try:
			vals = transpose(M_filtered)[a_id]
		except IndexError as e:
			probs.append([0 for a in a_values])
		else:
			probs.append([(vals.count(a)/len(vals)) for a in a_values])
	return probs

def train_classifier(data, values, a_ids, c_id):
	p_cs = p_a_mle(data, c_id, values[c_id])
	p_ai_given_cs = [p_ai_given_c_mle(data, a_id, c_id, values[a_id], values[c_id]) for a_id in a_ids]
	def trained_classifier(obj):
		p_c_given_ais = [0] * len(values[c_id])
		for c in values[c_id]:
			p_c_given_ais[c] = p_cs[c]
			for a_id in a_ids:
				p_c_given_ais[c] = p_c_given_ais[c] * p_ai_given_cs[a_id][c][obj[a_id]]
		return zero_one(p_c_given_ais)
	return trained_classifier



res = []
se = 1000
res.append(cross_validate(data, 24, train_classifier, unclassified, 10, seed))
while(se/math.sqrt(len(res)) > 0.005):
	res.append(cross_validate(data, 24, train_classifier, unclassified, 10, seed))
	mean = sum(res)/len(res)
	se = math.sqrt( (1/(len(res)-1)) * sum([(x - mean)**2 for x in res]) )
print mean