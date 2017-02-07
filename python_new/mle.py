from __future__ import division
import random

# import data
from data import data


def transpose(M):
	return [list(i) for i in zip(*M)]

def filter_by_class(M, class_id, class_val):
	return [row for row in M if row[class_id]==class_val]

def get_classes(M, a_id):
	M_t = transpose(M)
	return list(set(M_t[a_id]))

def p_a_mle(M, a_id):
	M_t = transpose(M)
	vals = M_t[a_id]
	return [vals.count(a)/len(vals) for a in get_classes(M, a_id)]

def p_ai_given_c_mle(M, a_id, c_id):
	probs = []
	for c in get_classes(M, c_id):
		M_filtered = filter_by_class(M, c_id, c)
		vals = transpose(M_filtered)[a_id]
		probs.append([vals.count(a)/len(vals) for a in range(30)])
	return probs

def train_classifier(data, a_ids, c_id):
	p_cs = p_a_mle(data, c_id)
	p_ai_given_cs = [p_ai_given_c_mle(data, a_id, c_id) for a_id in a_ids]
	def trained_classifier(obj):
		p_c_given_ais = [0] * 5
		for c in range(5):
			p_c_given_ais[c] = p_cs[c]
			for a_id in a_ids:
				p_c_given_ais[c] = p_c_given_ais[c] * p_ai_given_cs[a_id][c][obj[a_id]]
		return p_c_given_ais.index(max(p_c_given_ais))
	return trained_classifier

def split_data(data, k):
	split_data = [[] for i in range(k)]
	for i in range(len(data)):
		split_data[i%k].append(data[i])
	return split_data

def merge_datas(datas):
	res = []
	for data in datas:
		res = res + data
	return res


def cross_validate(data, c_id, classifier, k):
	random.shuffle(data)
	datas = split_data(data, k)
	res = []
	for i in range(k):
		training_data = merge_datas(datas[:i] + datas[i+1:])
		classifier = train_classifier(training_data, range(c_id), c_id)
		for obj in datas[i]:
			if classifier(obj) == obj[c_id]:
				res.append(1)
			else: 
				res.append(0)
	return sum(res)/len(res)


p_a_mle(data, 9)


print cross_validate(data, 24, train_classifier, 10)