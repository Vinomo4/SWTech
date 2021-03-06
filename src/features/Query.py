import argparse
import sys
import os
import pandas as pd
from joblib import load


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-author', '--author', type=str, help='Author to obtain the quality rating', required=True)
    return parser.parse_args()


def read_table():
    '''
    Objective:
        - Read clustering data
    Input:
        - None
    Output:
        - Clustering data
    '''

    # Define base path to data files
    path = '../../data/processed/'
    # Define base path to model files.
    path_mod = '../../models/'

    # Define path to the model_data_with_clusters table
    path_clusters_data = path + 'model_data_with_clusters.csv'

    # Ensure the input file exist
    assert os.path.isfile(path_clusters_data), f'{path_clusters_data} not found. Is it a file?'

    # Read clusterized data
    clusterized_data = pd.read_csv(path_clusters_data)

    return clusterized_data



if __name__ == '__main__':
    '''
    Objective:
        - Takes the author writen by the user and returns the quality metric and the cluster name of that user
    Input:
        - Author name
    Output:
        - Quality rating and name of the cluster
    '''

    args = parse_args()
    author = args.author
    # Read the clusterized data
    clusterized_data = read_table()
    # Load the prediction models.
    dt = load(path_mod+"Decision_tree_classifier.joblib")
    rf = load(path_mod+"Random_forest.joblib")
    # Search the author in the table
    quality_rating = clusterized_data.loc[clusterized_data['author'] == author,'quality_rating']
    if len(quality_rating) == 0:
        print("The author is not in the dataset")
    else:
        cluster_name = clusterized_data.loc[clusterized_data['author'] == author,'clusters']
        # The cluster of the author has been obtained by the clustering.
        if not pd.isnull(cluster_name):
            print("The quality rating of the author {} is {}. {} has {}".format(author,quality_rating[0],author,cluster_name[0]))
        # The author is new and no clustering operation has been executed yet. Thus, its cluster is obtained using the DT based models.
        else:
            aux = " "*3 + "·"
            print("Please, select the classifier you want to use:\n"+aux+"(1) - Decision Tree.\n"+aux+"(2) - Random forest.")
            try:
                method = int(input())
                if mehtod in [1,2]: break
            except: continue
            # Once the desired author and the model are selected, we proceed to compute their cluster prediction as well as its quality rating.
            model = dt if method == 1 else rf
            # Obtaining the obervation.
            X = clusterized_data.loc[clusterized_data['author'] == author].drop(["quality_rating","clusters"],axis = 1)
            # Obtaining the prediction.
            cluster_name = model.predict(X)
            # Obtaining the quality metric.
            for i,x in clusterized_data.iterrows():
                if x.clusters == cluster_name:
                    quality_rating = x.quality_rating
                    break
            print("The quality rating of the author {} is {}. {} has {}".format(author,quality_rating[0],author,cluster_name[0]))





# python3 Query.py --author 'Adrian Crum'
