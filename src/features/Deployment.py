import argparse
import sys
import os
import pandas as pd

sys.path.append('../features')
# Import useful functions for this script  
from tracking import track

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
    track("Defining path to data files")

    # Define base path to data files
    path = '../../temp_data/'

    # Define path to the model_data_with_clusters table
    path_clusters_data = path + 'model_data_with_clusters.csv'

    # Ensure the input file exist
    assert os.path.isfile(path_clusters_data), f'{path_clusters_data} not found. Is it a file?'
    
    track("Reading files")

    # Read clusterized data 
    clusterized_data = pd.read_csv(path_clusters_data)

    track("Finished reading files")
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

    track("-"*25 + "DEPLOYMENT" + "-"*25)
    args = parse_args()
    author = args.author
    # Read the clusterized data
    clusterized_data = read_table()

    # Search the author in the table
    try:
        quality_rating = clusterized_data.loc[clusterized_data['author'] == author,'quality_rating']
        cluster_name = clusterized_data.loc[clusterized_data['author'] == author,'cluster']
    except:
        print("The author is not in the dataset")
    
    print("The quality rating of the author {} is {}. It corresponds to the cluster {}".format(author,quality_rating,cluster)
