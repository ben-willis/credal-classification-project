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