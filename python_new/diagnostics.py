from __future__ import division
import random

def accuracy(classifications):
	results = [1 if (obj[0]==obj[1]) else 0 for obj in classifications]
	return sum(results)/len(results)

def mse(classifications):
	results = [(obj[0]-obj[1])**2 for obj in classifications]
	return sum(results)/len(results)

def unclassified(classifications):
	results = [1 if obj[0]==-1 else 0 for obj in classifications]
	return sum(results)/len(results)

def compare(classifications):
	n = len(classifications[0][0])
	results = [[[],[],[]],[[],[],[]],[[],[],[]]]
	for classification in classifications:
		for i in range(n):
			for j in range(n):
				results[i][j].append(classification[0][i] == classification[0][j])
	for i in range(n):
		for j in range(n):
			results[i][j] = sum(results[i][j])/len(results[i][j])
	return results

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

def transpose(M):
	return [list(i) for i in zip(*M)]

def get_classes(M, col_id):
	M_t = transpose(M)
	return list(set(M_t[col_id]))

def cross_validate(data, c_id, train_classifier, metric, k):
	values = [range(max(get_classes(data, col_id))+1) for col_id in range(c_id+1)]
	random.shuffle(data)
	datas = split_data(data, k)
	classifications = []
	for i in range(k):
		training_data = merge_datas(datas[:i] + datas[i+1:])
		classifier = train_classifier(training_data, values, range(c_id), c_id)
		classifications = classifications + [(classifier(obj), obj[c_id]) for obj in datas[i]]
	return metric(classifications)