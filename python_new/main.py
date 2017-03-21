from __future__ import division
import random, math

from data import data_cleaned as data
from diagnostics import accuracy, mse, unclassified, cross_validate, compare, single_accuracy, set_accuracy, indeterminate_output_size, determinacy

from mle import train_classifier as mle_classifier
from corrected import train_classifier as corrected_classifier
from idm import train_classifier as idm_classifier
from ncc import train_classifier as ncc_classifier

random.shuffle(data, lambda : 0.1)
s=0.1
print("\n---- s="+str(s)+" ----")
print("\nNCC")
cross_validate(data, 24, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)

s=0.5
print("\n---- s="+str(s)+" ----")
print("\nNCC")
cross_validate(data, 24, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)

s=1
print("\n---- s="+str(s)+" ----")
print("\nNCC")
cross_validate(data, 24, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)

s=2
print("\n---- s="+str(s)+" ----")
print("\nNCC")
cross_validate(data, 24, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)

s=5
print("\n---- s="+str(s)+" ----")
print("\nNCC")
cross_validate(data, 24, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)