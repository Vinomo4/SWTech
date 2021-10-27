# Import libraries and packages
import os
import sys
import pandas as pd
import numpy as np

# Define path with .py codes containing functions used in this script
sys.path.append('.')
sys.path.append('../features/')

# Import useful functions for this script
from tracking import track
from fun_validation import plot_quality_metrics,compare_classifiers

track("-"*25 + "VALIDATION" + "-"*25)

# Reading data
# Define path to data files

track("Defining path to data files")

# Define base path to data files
path = '../../data/processed/'

# Define path to the model_data_with_clusters table
path_clusters_data = path + 'model_data_with_clusters.csv'

# Ensure the input file exist
assert os.path.isfile(path_clusters_data), f'{path_clusters_data} not found. Is it a file?'


# Read the files
track("Reading files")

# Read clusterized data
clusterized_data = pd.read_csv(path_clusters_data)

track("Finished reading files")

# Validation

First, a validation of the different author types will be preformed.

track("Creating average quality dataset")
average_quality = (clusterized_data.groupby('clusters').agg(blocker_violations_mean = ('blocker_violations', 'mean'),
                                          blocker_violations_std = ('blocker_violations', 'std'),
                                          critical_violations_mean = ('critical_violations', 'mean'),
                                          critical_violations_std = ('critical_violations', 'std'),
                                          major_violations_mean = ('major_violations', 'mean'),
                                          major_violations_std = ('major_violations', 'std'),
                                          minor_violations_mean = ('minor_violations', 'mean'),
                                          minor_violations_std = ('minor_violations', 'std'),
                                          code_smells_mean = ('code_smells', 'mean'),
                                          code_smells_std = ('code_smells', 'std'),
                                          bugs_mean = ('bugs', 'mean'),
                                          bugs_std = ('bugs', 'std'),
                                          vulnerabilities_mean = ('vulnerabilities', 'mean'),
                                          vulnerabilities_std = ('vulnerabilities', 'std'),
                                          blocker_mean = ('blocker', 'mean'),
                                          blocker_std = ('blocker', 'std'),
                                          critical_mean = ('critical', 'mean'),
                                          critical_std = ('critical', 'std'),
                                          major_mean = ('major', 'mean'),
                                          major_std = ('major', 'std'),
                                          minor_mean = ('minor', 'mean'),
                                          minor_std = ('minor', 'std'),
                                          quality_rating = ('quality_rating','mean'))).reset_index()
track("Finished creating average quality dataset")
track("Creating plots of quality metrics")

# There will be three different plots. It is necessary to create the groups of the variables to be printed in the same plot
violation_metrics = ["blocker_violations", "critical_violations", "major_violations", "minor_violations"]
severity_metrics = ["blocker", "critical", "major", "minor"]
other_metrics = ["code_smells", "bugs", "vulnerabilities"]

# Order the quality rating from the best cluster to the words one. It allows to compare the values from the cluster with highest quality rating to the lowest one.3
sorted_average_quality = average_quality.sort_values(by=['quality_rating'],ascending = True)

plot_quality_metrics(sorted_average_quality, violation_metrics, [0, 5000, 10000, 15000, 20000, 25000])

plot_quality_metrics(sorted_average_quality, severity_metrics, [-1000, -500, 0, 500, 1000, 1500, 2000, 2500])

plot_quality_metrics(sorted_average_quality, other_metrics, [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000])
track("Finished creating plots of quality metrics")

#Then, a comparison between the performance of both classiers depending on the depth of the trees will also be executed.

compare_classifiers(clusterized_data,0.2)
