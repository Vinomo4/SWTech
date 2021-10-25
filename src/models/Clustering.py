
# Import libraries and packages
import numpy as np
import pandas as pd
import os
import sys
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from umap import UMAP
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import seaborn as sns
import sklearn

# Define path with .py codes containing functions used in this script

sys.path.append('./')
sys.path.append('../features')

# Import useful functions for this script
from tracking import track
from fun_models import save_plot,transform_dataset,WCSS_and_Elbow_Method,define_num_clusters,compute_PCA,compute_UMAP,plot_clusters

track("-"*25 + "CLUSTERING" + "-"*25)

# # Reading data
# #### Define path to data files
track("Defining path to data files")

# Define base path to data files
path = '../../data/interim/'

# Define path to the preprocesseded dataset that will be used in this script
path_preprocessed_data = path + 'model_data.csv'

# Ensure the input file exists
assert os.path.isfile(path_preprocessed_data), f'{path_preprocessed_data} not found. Is it a file?'

# #### Read the files

# Read table with preprocesseded data that will be used in this script
track("Reading preprocessed data")
preprocessed_data = pd.read_csv(path_preprocessed_data)
track("Finished reading preprocessed data")


# Drop the column containing the name of the author
data = preprocessed_data.loc[:, preprocessed_data.columns != 'author']
track("Author column was dropped")


cluster_cols = ['author_timezone', 'commit_message', 'n_commits', 'n_projects_c', 'complexity', 'cognitive_complexity', 'duplicated_blocks', 'duplicated_files',
                'duplicated_lines_density', 'files', 'comment_lines_density', 'n_measures', 'n_projects_m', 'effort', 'message','lines_added','lines_removed']

#quality_cols = ['violations', 'blocker_violations', 'critical_violations', 'major_violations', 'minor_violations', 'n_projects_i']
# info_violations, 'sqale_debt_ratio', 'code_smells', 'bugs', 'reliability_rating', 'vulnerabilities', 'security_rating',
#'blocker','critical', 'info', 'major', 'minor', 'issue_code_length', 'n_issues'

# # Model
# #### K-means with normalized data

track("Starting standardization of data")
# Standardization of data
track("Finished standardization of data")
standardized_data = transform_dataset(data[cluster_cols],type="standard")


# Compute the number of clusters and which cluster is every author
track("Starting WCSS and Elbow method for choosing the number of clusters")
clusters_none , number_of_clusters_none , silhouette_none = define_num_clusters(standardized_data,min_k=4, max_k=6, method="Normalized_data")
track("Finished WCSS and Elbow method for choosing the number of clusters")

# #### K-means with PCA data

# Compute PCA
track("Starting to compute PCA")
PCA_data = compute_PCA(standardized_data, min_var=0.95)
track("Finished computing PCA")


# Compute the number of clusters and which cluster is every author
track("Starting WCSS and Elbow method for choosing the number of clusters")
clusters_PCA, number_of_clusters_PCA, silhouette_PCA = define_num_clusters(PCA_data,min_k=4,max_k=6,method ="PCA")
track("Finished WCSS and Elbow method for choosing the number of clusters")

# #### K-means with UMAP data

# Compute UMAP
track("Starting to compute UMAP")
UMAP_data = compute_UMAP(standardized_data,n_neighbors=30,min_dist=0.01,n_components=10)
track("Finished computing UMAP")


# Compute the number of clusters and which cluster is every author
track("Starting WCSS and Elbow method for choosing the number of clusters")
clusters_UMAP, number_of_clusters_UMAP, silhouette_UMAP = define_num_clusters(UMAP_data,min_k=4,max_k=6,method ='UMAP')
track("Finished WCSS and Elbow method for choosing the number of clusters")


if silhouette_PCA > silhouette_UMAP and silhouette_PCA > silhouette_none:
    track("Computing PCA plot with K-Means clusters")
    plot_clusters(clusters_PCA, standardized_data,"PCA")
    preprocessed_data['clusters'] = clusters_PCA
elif silhouette_PCA < silhouette_UMAP and silhouette_UMAP > silhouette_none:
    track("Computing UMAP plot with K-Means clusters")
    plot_clusters(clusters_UMAP,  standardized_data,"UMAP")
    preprocessed_data['clusters'] = clusters_UMAP
else:
    track("Computing PCA and UMAP plots with K-Means clusters")
    plot_clusters(clusters_none,  standardized_data,"None")
    preprocessed_data['clusters'] = clusters_none

# ## Quality Metric calculation

track("Creating quality rating")
quality_rating_data = preprocessed_data.groupby('clusters').agg({
                            'blocker_violations': 'mean',
                            'critical_violations': 'mean',
                            'major_violations': 'mean',
                            'minor_violations': 'mean',
                            'blocker': 'mean',
                            'critical': 'mean',
                            'major': 'mean',
                            'minor': 'mean',
                            'code_smells': 'mean',
                            'bugs': 'mean',
                            'vulnerabilities': 'mean'
}).reset_index()

# Calculate ponderated mean of the violations variables
violations = quality_rating_data[["blocker_violations", "critical_violations", "major_violations", "minor_violations"]]
violations = violations*[0.5, 0.4, 0.07, 0.03]
violations = np.sum(violations, axis=1)
# Calculate ponderated mean of the severity issues variables
severity = quality_rating_data[["blocker", "critical", "major", "minor"]]
severity = severity*[0.5, 0.4, 0.07, 0.03]
severity = np.sum(severity, axis=1)
# Add violations and severity columns in the dataset
quality_rating_data['violations'] = violations
quality_rating_data['severity'] = severity
# Discard all types of violations and severity issues columns
quality_rating_data = quality_rating_data.drop(["clusters", "blocker_violations", "critical_violations", "major_violations", "minor_violations", "blocker", "critical", "major", "minor"], axis=1)
quality_rating_data
# compute the mean of each cluster
quality_rating_data = quality_rating_data[["violations", "code_smells",	"bugs",	"vulnerabilities",	"severity"]]
quality_rating_data
suma = np.sum(quality_rating_data, axis=1)

total = np.sum(suma)
quality_rating = 1 - (suma/total)
track("Finished creating quality rating")



# # Saving quality metric

# Saving the quality metric to the cluster data
dic_quality = {}
for i in range(len(quality_rating)):
    dic_quality[i] = quality_rating[i]

preprocessed_data['quality_rating'] = preprocessed_data['clusters'].map(dic_quality)




# # Assigning name to the clusters

# Assigning name to the clusters, depending on the quality rating
dic_name_clusters = {}

for i in range(len(quality_rating)):
    if quality_rating[i] <= 0.2:
        dic_name_clusters[i] = 'Extremely bad programming skills'
    elif quality_rating[i] <= 0.4 and quality_rating[i] > 0.2:
        dic_name_clusters[i] = 'Poor programming skills'
    elif quality_rating[i] <= 0.6 and quality_rating[i] > 0.4:
        dic_name_clusters[i] = 'Bad programming skills'
    elif quality_rating[i] <= 0.8 and quality_rating[i] > 0.6:
        dic_name_clusters[i] = 'Average programming skills'
    elif quality_rating[i] <= 0.9 and quality_rating[i] > 0.8:
        dic_name_clusters[i] = 'Good programming skills'
    else:
        dic_name_clusters[i] = 'Excellent programming skills'

preprocessed_data['clusters'] = preprocessed_data['clusters'].map(dic_name_clusters)




# # Saving data with clusters

# Lastly, the final dataframe with the cluster variable and the quality rating is written in the suitable folder.

try: os.mkdir("../../data/processed/")
except: pass
preprocessed_data.to_csv("../../data/processed/model_data_with_clusters.csv", index = False)
