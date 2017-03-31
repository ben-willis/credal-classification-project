from __future__ import division, print_function
import random

def remove_row(M, j):
	return M[:j] + M[j+1:]

def remove_rows_with_missing_values(M):
	for j in range(len(M)-1, -1, -1):
		if -1 in M[j]:
			M = remove_row(M, j)
	return M

def accuracy(classifications):
	results = [1 if (obj[0]==obj[1]) else 0 for obj in classifications]
	return {
		"result": 100*sum(results)/len(results),
		"name": "Accuracy"
	}

def mse(classifications):
	results = []
	for classification in classifications:
		if classification[1] != -1:
			results.append((classification[0]-classification[1])**2)
	return {
		"result": sum(results)/len(results),
		"name": "MSE"
	}

def unclassified(classifications):
	results = [1 if obj[1]==-1 else 0 for obj in classifications]
	return {
		"result": sum(results)/len(results),
		"name": "Unclassified"
	}

def confussion(classifications):
	results = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
	for classification in classifications:
		results[classification[0]][classification[1]] = results[classification[0]][classification[1]] + 1
	total = sum([sum(row) for row in results])
	results = [[item/total for item in row] for row in results]
	for row in results:
		for item in row:
			print(str(round(item*100, 2)) + "\%", end=" & ")
		print('\\\\')
	return {
		"result": results,
		"name": "Confusion"
	}

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

def single_accuracy(classifications):
	results = []
	for classification in classifications:
		if len(classification[1]) != 1:
			continue;
		if classification[0] == classification[1][0]:
			results.append(1)
		else:
			results.append(0)
	return {
		"result": "null" if (len(results)==0) else 100*sum(results)/len(results),
		"name": "Single Accuracy"
	}

def indeterminate_output_size(classifications):
	results = []
	for classification in classifications:
		if len(classification[1]) == 1:
			continue;
		results.append(len(classification[1]))
	return {
		"result": sum(results)/len(results),
		"name": "Indeterminate Output Size"
	}

def set_accuracy(classifications):
	results = []
	for classification in classifications:
		if len(classifications[1]) == 1:
			continue;
		if classification[0] in classification[1]:
			results.append(1)
		else:
			results.append(0)
	return {
		"result": 100*sum(results)/len(results),
		"name": "Set Accuracy"
	}

def dual_accuracy(classifications):
	results = []
	for classification in classifications:
		if len(classifications[1]) != 2:
			continue;
		if classification[0] in classification[1]:
			results.append(1)
		else:
			results.append(0)
	return {
		"result": 100*sum(results)/len(results),
		"name": "Dual Accuracy"
	}

def determinacy(classifications):
	results = [1 if len(classification[1]) == 1 else 0 for classification in classifications]
	return {
		"result": 100*sum(results)/len(results),
		"name": "Determinacy"
	}

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

def cross_validate(data, c_id, train_classifier, metrics, k, s):
	values = [range(max(get_classes(data, col_id))+1) for col_id in range(c_id+1)]
	datas = split_data(data, k)
	classifications = []
	for i in range(k):
		training_data = merge_datas(datas[:i] + datas[i+1:])
		test_data = remove_rows_with_missing_values(datas[i])
		classifier = train_classifier(training_data, values, range(c_id), c_id, s)
		classifications = classifications + [(obj[c_id], classifier(obj)) for obj in test_data]
	for metric in metrics:
		res = metric(classifications)
		print(res['name'], end=": ")
		print(res['result'])