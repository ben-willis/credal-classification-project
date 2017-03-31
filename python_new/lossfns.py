import random

def zero_one(class_probabilities):
	if class_probabilities[1:] == class_probabilities[:-1]:
		return -1
	return class_probabilities.index(max(class_probabilities))

def squared_diff(class_probabilities):
	mean = 0
	for i in range(len(class_probabilities)):
		mean = mean + class_probabilities[i] * i
	return mean

def absolute_diff(class_probabilities):
	losses = []
	for class_estimate in range(len(class_probabilities)):
		losses.append(sum([abs(class_estimate - i) * class_probabilities[i] for i in range(len(class_probabilities))]))
	return losses.index(min(losses))

def custom(class_probabilities):
	loss_matrix = [[0,1,1,1,1,1],[10,0,1,1,1,1],[20,10,0,1,1,1],[50,25,10,0,1,1],[80,40,20,10,0,1],[100,50,30,20,10,0]]
	losses = []
	for class_estimate in range(len(class_probabilities)):
		losses.append(sum([loss_matrix[i][class_estimate] * class_probabilities[i] for i in range(len(class_probabilities))]))
	return losses.index(min(losses))

def credal(class_probability_intervals):
	dominated = []
	for p_c_intervala in class_probability_intervals:
		dominated.append(False)
		for p_c_intervalb in class_probability_intervals:
			if p_c_intervala[1] < p_c_intervalb[0]:
				dominated[-1] = True
				break;
	return [i for i in range(len(class_probability_intervals)) if not dominated[i]]

def upper(class_probability_intervals):
	class_probabilities = [list(t) for t in zip(*class_probability_intervals)][1]
	if class_probabilities[1:] == class_probabilities[:-1]:
		return -1
	return class_probabilities.index(max(class_probabilities))

def lower(class_probability_intervals):
	class_probabilities = [list(t) for t in zip(*class_probability_intervals)][0]
	if class_probabilities[1:] == class_probabilities[:-1]:
		return -1
	return class_probabilities.index(max(class_probabilities))

