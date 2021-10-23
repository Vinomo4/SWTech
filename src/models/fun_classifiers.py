# Import libraries and packages
import numpy as np
import pandas as pd
import seaborn as sn
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import tree

def split_data(data,part_size):
    '''
    Objective:
        - Split the data into training and test partitions.
    Input:
        - data : Dataframe that contains the values to split.
        - part_size : Percentage of values reserved for testing.
    Output:
        - X,y vectors, splitted into training and test.
    '''
    X_train, X_test, Y_train, Y_test = train_test_split(data.drop(labels = "clusters",axis =1), data['clusters'], random_state=0, test_size = part_size)
    return X_train,X_test, Y_train, Y_test

def train_decision_tree(data,depth = 3):
    '''
    Objective:
        - Create a decision tree that classifies authors into their respective
          cluster acording to their commit information.
    Input:
        - data : List containing the X,Y training vectors.
        - depth : Maximum depth of the classifier.

    Output:
        - Trained Decision Tree Classifier.
    '''
    X_train,Y_train = data[0],data[1]
    # Creating the decission tree classifer.
    dtc = DecisionTreeClassifier(max_depth = depth, random_state = 0)
    dtc.fit(X_train, Y_train)
    # An image of the DTC indicating the decision threshold is stored.
    fn=X_train.columns
    cn= sorted(Y_train.unique())
    plt.figure(figsize=(20,12))
    tree.plot_tree(dtc,
                   feature_names = fn,
                   class_names=cn,
                   filled = True,
                   fontsize=10);
    path = '../../reports/figures/models/Decision_tree_classifier/'
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path+'Decision_tree.png')
    return dtc

def train_random_forest(data,depth = 3, n_trees = 100):
    '''
    Objective:
         - Create a random forest that classifies authors into their respective
          cluster acording to their commit information.
    Input:
        - data : Dataframe that contains the values for the tree generation.
        - depth : Maximum depth of the classifier.
        - n_trees: Number of trees ensembled.

    Output:
        - Trained Random Forest.
    '''
    X_train,Y_train = data[0],data[1]
    # Creating the random forest.
    rf = RandomForestClassifier(n_estimators=n_trees,
                                max_depth = depth,
                                random_state=0)
    rf.fit(X_train, Y_train)
    return rf

def generate_confusion_heatmap(pred,gt,method):
    '''
    Objective:
         - Generate a heatmap where the rows are the true labels, the
         columns the predicted and in each cell (e.g (i,j)) the percentage of
         values that having i as true label have been predicted as j.
    Input:
        - pred : Vector containing the predictions of the model.
        - gt: Pandas series containing the ground truth values.
        - method: Type of classifier used (Random Forest or Decision Tree Classifier)
    Output:
        - None.
    '''
    c = gt.nunique()
    #First,we create the confusion marix.
    conf_matrix = np.zeros((c,c))
    # To each cluster value a number is associated.
    labels = sorted(gt.unique())
    dict_labels = {}
    for i,lab in enumerate(labels):
        dict_labels[lab] = i
    # The ground truth series is converted to list
    y = gt.values
    # Now, the matrix is filled.
    for i in range(len(pred)):
        conf_matrix[dict_labels[y[i]]][dict_labels[pred[i]]]+=1
    for i in range(c):
        conf_matrix[i] /= sum(conf_matrix[i])

    ax = plt.axes()
    sn.heatmap(conf_matrix, annot=True, fmt=".3f", ax = ax,xticklabels=labels, yticklabels=labels)
    ax.set_title('Confusion matrix')
    path = '../../reports/figures/models/Decision_tree_classifier/'
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path+'Confussion_matrix_'+method+'.png')
