import pandas as pd

# import data
from data import df
# import mle classifier
from mle import train_classifier as mle_classifier
# import cross validator
from cv import cross_validate

# determine the accuracy of mle classifier on the df using 10-fold cross validation
print cross_validate(df, mle_classifier, 10)