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

def split_data(data,part_size, seed):
    '''
    Objective:
        - Split the data into training and test partitions.
    Input:
        - data : Dataframe that contains the values to split.
        - part_size : Percentage of values reserved for testing.
        - seed: Integer used to establish the seed and obtain replicable partitions
    Output:
        - X,y vectors, splitted into training and test.
    '''
    X_train, X_test, Y_train, Y_test = train_test_split(data.drop(labels = "clusters",axis =1), data['clusters'], random_state=seed, test_size = part_size)
    return X_train,X_test, Y_train, Y_test

def generate_confusion_matrix(pred,gt):
        '''
        Objective:
             - Generate a confusion matrix where the rows are the true labels, the
             columns the predicted and in each cell (e.g (i,j)) the percentage of
             values that having i as true label have been predicted as j.
        Input:
            - pred : Vector containing the predictions of the model.
            - gt: Pandas series containing the ground truth values.
        Output:
            - conf_matrix: The confusion matrix itself.
            - labels: The labels used in the confusion matrix.
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
        return conf_matrix, labels

def train_decision_tree(data,part_size,depth = 3):
    '''
    Objective:
        - Create a decision tree that classifies authors into their respective
          cluster acording to their commit information.
    Input:
        - data :Dataframe that contains the values used for modeling.
        - part_size: Percentage of values reserved for testing.
        - depth : Maximum depth of the classifier.

    Output:
        - Trained Decision Tree Classifier.
        - Averaged confussion matrix.
    '''
    cm_list = []
    # Training with all the data.
    if not part_size:
        dtc = DecisionTreeClassifier(max_depth = depth, random_state = 0)
        X_train, Y_train = data.drop(labels = "clusters",axis =1), data['clusters']
        dtc.fit(X_train,Y_train)
        return dtc,None,None
    else:
        for i in range(10):
            X_train,X_test, Y_train, Y_test = split_data(data,part_size,i)
            # Creating the decission tree classifer.
            dtc = DecisionTreeClassifier(max_depth = depth, random_state = 0)
            # Training
            dtc.fit(X_train, Y_train)
            # Prediction
            pred = dtc.predict(X_test)
            # Confussion matrix computation
            cm,labels = generate_confusion_matrix(pred, Y_test)
            cm_list.append(cm)
        # An image of the DTC indicating the decision threshold is stored.
        fn=X_train.columns
        cn= sorted(Y_train.unique())
        plt.figure(figsize=(20,12), facecolor = "white")
        tree.plot_tree(dtc,
                          feature_names = fn,
                          class_names=cn,
                          filled = True,
                          fontsize=10,
                          rounded = True);
        path = '../../reports/figures/models/Classifiers/'
        if not os.path.isdir(path):
            os.makedirs(path)
        plt.savefig(path+'Decision_tree.png')
        return dtc, sum(cm_list)/len(cm_list), labels

def train_random_forest(data,part_size,depth = 3, n_trees = 100):
    '''
    Objective:
         - Create a random forest that classifies authors into their respective
          cluster acording to their commit information.
    Input:
        - data : Dataframe that contains the values used for modeling.
        - part_size: Percentage of values reserved for testing.
        - depth : Maximum depth of the classifier.
        - n_trees: Number of trees ensembled.

    Output:
        - Trained Random Forest.
    '''
    # Training with all the data
    if not part_size:
        rf = RandomForestClassifier(n_estimators=n_trees,
                                    max_depth = depth,
                                    random_state=0)
        X_train, Y_train = data.drop(labels = "clusters",axis =1), data['clusters']
        rf.fit(X_train,Y_train)
        return rf,None,None
    cm_list = []
    for i in range(10):
        X_train,X_test, Y_train, Y_test = split_data(data,part_size,i)
        # Creating the random forest.
        rf = RandomForestClassifier(n_estimators=n_trees,
                                    max_depth = depth,
                                    random_state=0)
        # Training
        rf.fit(X_train, Y_train)
        # Prediction
        pred = rf.predict(X_test)
        # Confussion matrix computation
        cm,labels = generate_confusion_matrix(pred, Y_test)
        cm_list.append(cm)
    return rf,sum(cm_list)/len(cm_list),labels

def generate_confusion_heatmap(conf_matrix,labels,method):
    '''
    Objective:
         - Generate a heatmap where the rows are the true labels, the
         columns the predicted and in each cell (e.g (i,j)) the percentage of
         values that having i as true label have been predicted as j.
    Input:
        - conf_matrix: Confussion matrix of the model.
        -labels: Labels to use in the confusion heatmap.
        - method: Type of classifier used (Random Forest or Decision Tree Classifier)
    Output:
        - None.
    '''
    plt.figure(figsize=(20,12), facecolor = "white")
    ax = plt.axes()
    sn.heatmap(conf_matrix, annot=True, fmt=".3f", ax = ax,xticklabels=labels, yticklabels=labels)
    ax.set_title('Confusion matrix')
    path = '../../reports/figures/models/Classifiers/'
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path+'Confussion_matrix_'+method+'.png')
