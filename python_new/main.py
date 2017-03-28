from __future__ import division
import random, math

from data import transpose, remove_rows_with_missing_values, unclean_data, clean_data, reduced_data
from diagnostics import accuracy, mse, unclassified, cross_validate, compare, confussion, single_accuracy, set_accuracy, dual_accuracy, indeterminate_output_size, determinacy

from mle import train_classifier as mle_classifier
from corrected import train_classifier as corrected_classifier
from idm import train_classifier as idm_classifier
from ncc import train_classifier as ncc_classifier

random.shuffle(unclean_data, lambda : 0.2)

reduced_data = transpose(unclean_data)
reduced_data = remove_rows_with_missing_values(reduced_data)
reduced_data = transpose(reduced_data)

clean_data = remove_rows_with_missing_values(unclean_data)

s=1
# cross_validate(data, 24, corrected_classifier, [confussion], 10, s)
print("----- Without Missing Values -----")
cross_validate(clean_data, len(clean_data[0]) - 1, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)
print("-----  With Missing Values   -----")
cross_validate(unclean_data, len(unclean_data[0]) - 1, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)
print("----- Without Missing Columns -----")
cross_validate(reduced_data, len(reduced_data[0]) - 1, ncc_classifier, [single_accuracy, set_accuracy, indeterminate_output_size, determinacy], 10, s)