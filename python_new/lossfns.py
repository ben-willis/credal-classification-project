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
	left_probs = 0
	possible_medians = []
	for i in range(len(class_probabilities)):
		if (left_probs + class_probabilities[i] >= 0.5) and (1-left_probs >= 0.5):
			possible_medians.append(i)
		left_probs = left_probs + class_probabilities[i]
	if possible_medians == []:
		bleh = 0;
		for prob in class_probabilities:
			print str(left_probs+class_probabilities[i]) + ", " + str(left_probs)
			bleh = bleh + prob;
	return random.choice(possible_medians)

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

